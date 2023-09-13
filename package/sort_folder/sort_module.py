from pathlib import Path
from itertools import chain
import shutil
import re
from prompt_toolkit import prompt

from utils.tool_kit import RainbowLexer, get_completer
from utils.cls_clear import clear

FILE_EXTENSIONS = {
    'images': {'.jpeg', '.png', '.jpg', '.svg'},
    'video': {'.avi', '.mp4', '.mov', '.mkv'},
    'documents': {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'},
    'audio': {'.mp3', '.ogg', '.wav', '.amr'},
    'archives': {'.zip', '.gz', '.tar'}
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

def normalize(name: str) -> str:
    """
    Normalize a given string by replacing non-alphanumeric characters with underscores.

    Args:
        name (str): The input string to be normalized.
    Returns:
        str: The normalized string with non-alphanumeric characters replaced by underscores.
    """
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name

def new_path_name(ex: Path) -> Path:
    """
    Create a new path name for a file by normalizing its stem and keeping the original suffix.

    Args:
        ex (Path): The original path to the file.
    Returns:
        Path: The new path with a normalized stem and the original suffix.
    """
    new_name = normalize(ex.stem) + ex.suffix  # новое имя + суфикс
    new_ex = ex.rename(ex.parent / new_name)  # переименование файлов + присваеваем новий путь
    return new_ex

def get_new_folder_name(ex: Path) -> str:
    """
    Get a new folder name based on the file extension of the given path.

    Args:
        ex (Path): The original file path.
    Returns:
        str: The new folder name based on the file extension.
    """
    name_dir = ""
    for key, val in FILE_EXTENSIONS.items():
        if ex.suffix in val:
            name_dir = key
            break
    if not name_dir:  # если нет совпадений по константе
        name_dir = "others"
    return name_dir

def replace_file_new_dir(ex: Path, name_dir: str, main_path: Path) -> Path:
    """
    Replace a file into a new directory based on the provided folder name.

    Args:
        ex (Path): The original file path.
        name_dir (str): The name of the target folder.
        main_path (Path): The main directory path.
    Returns:
        Path: The new path of the file in the specified folder.
    """
    new_dir_path = main_path / name_dir  # путь к новой папке для ее создание и переноса файлов
    new_dir_path.mkdir(exist_ok=True)  # создаем новую папку если такой нет
    new_ex_path = ex.replace(new_dir_path / ex.name)  # перенос файлов в папки по категориям
    return new_ex_path

def extract_archive(archive_path: Path, del_archive=True):
    """
    Extract the contents of an archive file to a target directory.

    Args:
        archive_path (Path): The path to the archive file.
        del_archive (bool, optional): Whether to delete the archive file after extraction. Defaults to True.
    """
    target_dir = archive_path.parent / archive_path.stem  # путь для созданием папки с именем архива
    target_dir.mkdir(exist_ok=True)  # создаем папку для архива
    try:
        shutil.unpack_archive(archive_path, target_dir)  # распаковка
        if del_archive:  # удаляем архив по флагу после распаковки
            archive_path.unlink()
    except ValueError:
        print(f"Failed to unpack the archive: {archive_path.name}")
    except shutil.ReadError:
        print(f"Archive - {archive_path.stem} not unpacked\tunknown extension({archive_path.suffix})")  



def sort_folder(path: Path, my_dict_files: dict=None, main_path: Path | None=None) -> dict[str, list[tuple[str]]]:
    """
    Recursively sorts files in a directory by category.

    This function recursively traverses a directory and sorts its files into categories based on their extensions.
    It also renames files and directories as needed and can handle archives by extracting them.

    Args:
        path (Path): The path to the directory to be sorted.
        my_dict_files (dict, optional): A dictionary to store file information. Defaults to None.
        main_path (Path | None, optional): The main path of the directory. Defaults to None.
    Returns:
        dict[str, list[tuple[str]]]: A dictionary containing file information categorized by extension.
    """
    if main_path is None : main_path = path
        
    for item in path.iterdir():
        if item.is_file():
            item = new_path_name(item)  # переименование файла
            name_dir = get_new_folder_name(item)  # имя для новой папки
            item = replace_file_new_dir(item, name_dir, main_path)  # создание папок + перемещение файлов
            if name_dir == "archives":  
                extract_archive(item)  # разпаковка + по умолчанию флаг на удаление

            if my_dict_files is None:  my_dict_files : dict = {}  # создаем словарь на первом заходе
            if name_dir not in my_dict_files:  # если нет ключа создаем ключ:спиок
                my_dict_files[name_dir] = [(item.stem, item.suffix)] # key - name_dir : val - list[tuple()]
            else:
                my_dict_files[name_dir].append((item.stem, item.suffix))

        elif item.is_dir() and (item.name not in FILE_EXTENSIONS):  # проверка на папку и она не из наших ключей
            my_dict_files = sort_folder(path / item.name, my_dict_files, main_path)  # рекурсивний заход + my_dict_files-> категория : [файли]

            if not any(item.iterdir()):  # проверка на пустую папку
                item.rmdir()  # удаляем папку(пустую)
    return my_dict_files

def get_set_keys(norm_dict: dict) -> set:
    """
    Get a set of all keys from a nested dictionary.

    Args:
        norm_dict (dict): The input dictionary.
    Returns:
        set: A set containing all keys from the nested dictionary.
    """
    return set(chain.from_iterable(norm_dict.values()))

def dict_normalize(my_dict_files: dict[str, list[tuple[str]]], val="file", res_dict: dict | None=None):
    """
    Normalize a nested dictionary and extract values by key.

    Args:
        my_dict_files (dict[str, list[tuple[str]]]): The input dictionary.
        val (str, optional): The value to extract, either "file" or "ext". Defaults to "file".
        res_dict (dict, optional): A dictionary to store the normalized results. Defaults to None.
    Returns:
        dict: A dictionary containing the normalized values extracted by key.
    """
    if res_dict is None : res_dict = {}
    if val == "file":
        i = 0
    elif val == "ext":
        i = 1

    for folder, list_tupl_file_ex in my_dict_files.items():
        res_dict.update({folder : list(map(lambda x: x[i], list_tupl_file_ex))})
    return res_dict    

def show_sort_files(my_dict_files_ext: dict[str, list[tuple[str]]]) -> str:
    """
    Generate a string representation of files sorted by category.

    Args:
        my_dict_files_ext (dict[str, list[tuple[str]]]): A dictionary containing files sorted by category.
    Returns:
        str: A formatted string displaying files categorized by folder.
    """
    res_list = []
    for folder, files in dict_normalize(my_dict_files_ext, val="file").items():
        res_list.append("{:<10}: {}".format(folder, ', '.join(files)))
    sep = '\n\t'
    return f"\nlist of files in a sorted directory by category:\n\t{f'{sep}'.join(res_list)}"    

def show_knolege_ext(my_dict_files_ext: dict[str, list[tuple[str]]]) -> str:
    """
    Generate a string listing all known extensions in a sorted directory.

    Args:
        my_dict_files_ext (dict[str, list[tuple[str]]]): A dictionary containing files and their extensions sorted by category.
    Returns:
        str: A formatted string displaying known extensions in the sorted directory.
    """
    bot_ext: set = get_set_keys(FILE_EXTENSIONS) 
    sort_ext: set  = get_set_keys(dict_normalize(my_dict_files_ext, val="ext"))
    know_ext = bot_ext.intersection(sort_ext)
    if len(know_ext) == 0: know_ext = ["List is empty"]
    return f"\nList of all known extensions in a sorted directory:\n \
            \n\t{' | '.join(know_ext)}"

def show_unknow_ext(my_dict_files_ext: dict[str, list[tuple[str]]]) -> str:
    """
    Generate a string listing extensions not known to this script in a sorted directory.

    Args:
        my_dict_files_ext (dict[str, list[tuple[str]]]): A dictionary containing files and their extensions sorted by category.
    Returns:
        str: A formatted string displaying extensions not known to this script in the sorted directory.
    """
    bot_ext: set = get_set_keys(FILE_EXTENSIONS) 
    sort_ext: set  = get_set_keys(dict_normalize(my_dict_files_ext, val="ext"))
    know_ext = bot_ext.intersection(sort_ext)
    unknow_ext = sort_ext.difference(know_ext)
    if len(unknow_ext) == 0: unknow_ext = ["List is empty"]
    return f"\nList of all extensions not known to this script:\n \
            \n\t{' | '.join(unknow_ext)}"

def show_bot_ext(*args) -> str:
    return f"data bot kholege extension :\n{' | '.join(get_set_keys(FILE_EXTENSIONS))}"

def sort_unk_command(*args) -> str:
    return 'Unknown command\n'

def sort_exit(*args) -> str:
    return "\nsorting is closed go to the main menud\n"

def sort_help(*args) -> str:
    info = "\n".join(INFO) #костиль
    return f'Commans for info after sort your folder\n\n{info}'

SORT_COMMANDS = {
    show_bot_ext : ["bot ext", "data", "bot data",],
    show_sort_files : ["show file", "file" ],
    show_knolege_ext : ["show ext", "ext", "my ext", "extensions", "know"],
    show_unknow_ext : ["unk", "unknown", "unk ext",],
    sort_exit : ["menu", "back", "fin",],
    sort_help :["help"]
}
#костиль
INFO = [
    "data - Displays extended information about the bot, including its data.",
    "file - Shows a list of files and folders in the current directory.",
    "ext - Displays a list of known file extensions and the programs associated with them.",
    "unk - Displays a list of unknown (unsupported) file extensions.",
    "menu - Returns to the main menu or exits the current submenu.",
    "help - Displays help information about available commands in the current submenu.",

]
def parser_cm(user_input: str):
    for func, comm in SORT_COMMANDS.items():
        if user_input.strip().lower() in comm:
            return func
    return sort_unk_command   

Completer = get_completer(SORT_COMMANDS.values())

def main_sort():
    clear()
    print(sort_help())
    path_input = input("\nEnter full path to you dir, will be sort >>>")
    if Path(path_input).is_dir():
        path = Path(path_input)
        dir_data: dict[str, list[tuple[str]]] = sort_folder(path)
        print(f'\nYour folder "{path.stem}" has been sorted\n')
        while True:
            # user_input = input("\nSorted info/back to menu>>>")
            user_input = prompt(
                message="\nSorted info or menu >>>",
                completer=Completer,                
                lexer=RainbowLexer("#FFFF00")               
                )
            if not user_input or user_input.isspace():
                continue

            func = parser_cm(user_input)
            print(func(dir_data)) 

            if func == sort_exit:
                break

    elif path_input in SORT_COMMANDS.get(sort_exit):
        print(sort_exit()) # back to menu           
    else:
        print("not corect path")
        main_sort() # костиль

if __name__ == "__main__":
    main_sort()