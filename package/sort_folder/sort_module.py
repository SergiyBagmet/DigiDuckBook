from pathlib import Path
from itertools import chain
import shutil
import re


# известние файли для сортировки
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
    транлитерация кирилици
    замена всего кроме латинского алфавита и чисел на _
    """
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


def new_path_name(ex: Path) -> Path:
    """
    переименование по транслиту + "_"
    возврат нового пути(../файл.суф)
    """
    new_name = normalize(ex.stem) + ex.suffix  # новое имя + суфикс
    new_ex = ex.rename(ex.parent / new_name)  # переименование файлов + присваеваем новий путь
    return new_ex


def get_new_folder_name(ex: Path) -> str:
    """
    получаем имя для новой папки(по расширению файла)
    соответствующей файловой группе
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
    сознаем новую папку если такой нет
    перенос файла -> возврат нового пути
    """
    new_dir_path = main_path / name_dir  # путь к новой папке для ее создание и переноса файлов
    new_dir_path.mkdir(exist_ok=True)  # создаем новую папку если такой нет
    new_ex_path = ex.replace(new_dir_path / ex.name)  # перенос файлов в папки по категориям
    return new_ex_path


def extract_archive(archive_path: Path, del_archive=True):
    """
    разархивируем архив в папку с именем архива
    с флагом на удаление архива + ловим ошибку
    """
    target_dir = archive_path.parent / archive_path.stem  # путь для созданием папки с именем архива
    target_dir.mkdir(exist_ok=True)  # создаем папку для архива
    try:
        shutil.unpack_archive(archive_path, target_dir)  # распаковка
        if del_archive:  # удаляем архив по флагу после распаковки
            archive_path.unlink()
    except ValueError:
        print(f"Не удалось разпаковать архив : {archive_path.name}")
    except shutil.ReadError:
        print(f"Архив - {archive_path.stem} не распакован\tнеизвестное расширение({archive_path.suffix})")




def sort_folder(path: Path, main_path: Path, my_dict_files=None) -> dict:
    """
    основной рекурсивний проход
    всех папок и файлов
    """
    for item in path.iterdir():
        if item.is_file():

            item = new_path_name(item)  # переименование файла

            name_dir = get_new_folder_name(item)  # имя для новой папки

            item = replace_file_new_dir(item, name_dir, main_path)  # создание папок + перемещение файлов

            if name_dir == "archives":  # если категория ахиви(файл можно разпаковать TODO list from shatil)
                extract_archive(item)  # разпаковка + по умолчанию флаг на удаление

            # get_data: set of ex +  my_dict_files-> категория : [файли] TODO отдельная функция?
            # my_extens.add(item.suffix)  # заполнение сета расширений
            if my_dict_files is None:  my_dict_files : dict = {}  # создаем словарь на первом заходе
            # sep_name_sufix = "".join(item.stem, item.suffix)
            if name_dir not in my_dict_files:  # если нет ключа создаем ключ:спиок
                my_dict_files[name_dir] = [(item.stem, item.suffix)] 
            else:
                my_dict_files[name_dir].append((item.stem, item.suffix))


        elif item.is_dir() and (item.name not in FILE_EXTENSIONS):  # проверка на папку и она не из наших ключей
            my_dict_files = sort_folder(path / item.name, main_path, my_dict_files)  # рекурсивний заход + my_dict_files-> категория : [файли]

            if not any(item.iterdir()):  # проверка на пустую папку
                item.rmdir()  # удаляем папку(пустую)

    return my_dict_files

def bot_ext() -> set:
    return set(chain.from_iterable(FILE_EXTENSIONS.values()))

def get_dict(my_dict_files: dict[str, list[tuple[str, str]]], val="file", res_dict: dict | None=None):
    if res_dict is None : res_dict = {}
    if val == "file":
        i = 0
    elif val == "ext":
        i = 1

    for folder, list_tupl_file_ex in my_dict_files.items():
        res_dict | {folder : list(map(lambda x: x[i], list_tupl_file_ex))}
    return res_dict    
                
def show_bot_ex(*args) -> str:
    return f"data bot kholege extension :\n{' | '.join(bot_ext())}"

def show_sort_file(my_dict_files: dict[str, list[tuple[str, str]]]) -> str:
    res_list = []
    for folder, list_tupl_file_ex in my_dict_files.items():
        file_names = ", ".join(list(map(lambda x: x[0], list_tupl_file_ex)))
        res_list.append("{:<10}: {}".format(folder, file_names))
    return "\n".join(res_list)    

def show_knolege_ex(my_dict_files: dict[str, list[tuple[str, str]]]) -> str:
    pass

def sort_unk_command(*args) -> str:
    return 'Unknown command'

def sort_exit(*args) -> str:
    return "change to menu\n\n"


SORT_COMMANDS = {
    show_bot_ex : ["bot ext", "data", "bot extensions",],
    sort_exit : ["menu", ],
    show_sort_file : ["show file", "file" ],
    show_knolege_ex : ["show ext", "ext", "my ext", "extensions", "ext"],
    # show_unknow_ex : [],
}

def parser_cm(user_input: str):
    """
    TODO
    """
    for func, com in SORT_COMMANDS.items():
        if user_input.strip().lower() in com:
            return func
    return sort_unk_command   

def sort_main():
    """
    TODO
    """  
    path_input = input("Enter full path to you dir, will be sort or exit\n>>>")
    if Path(path_input).is_dir():
        path = Path(path_input)
        dir_data: dict = sort_folder(path, path)

        while True:
            user_input = input(">>>")
            if not user_input or user_input.isspace():
                continue
            func = parser_cm(user_input)  
            print(func(dir_data))

            if func == sort_exit:
                break

    elif path_input in SORT_COMMANDS.get(sort_exit):
        print(sort_exit())           
    else:
        print("not corect path")
        sort_main()

if __name__ == "__main__":
    sort_main()