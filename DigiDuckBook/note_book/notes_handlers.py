from functools import wraps
import re, json
from pathlib import Path
from prompt_toolkit import prompt

from DigiDuckBook.note_book.notes_oop import NoteTag, NoteBody, RecordNote, NotesBook
from DigiDuckBook.utils.data_json import DIR_DATA, get_obj, BookEncoder
from DigiDuckBook.utils.tool_kit import RainbowLexer, get_completer
from DigiDuckBook.utils.cls_clear import clear


file_notes_json = Path(DIR_DATA) / "notes_book.json"
n_book: NotesBook = get_obj(file_notes_json, NotesBook) 

def input_error(func):
    @wraps(func)
    def wrapper(*args):
        """
        Decorator gets errors of functions,
        lack of arguments and raise of errors
        and return them to print
        """
        try:
            return func(*args)
        except IndexError:
            command, formula = COMMANDS_HELP.get(func.__name__)
            command = '/'.join(command)
            return (f"Wrong input for this command [{command}]\n"
                    f"for example:\t[{command}] {formula}"
                    )
        except ValueError as err:
            return f"Input error: {str(err)}."
        except KeyError as err:
            return f"Enter the note or note tag: {str(err)}."
    return wrapper


@input_error
def add_note_record_handler(data: list[str]) -> str:
    """
    Add a new note to the notes book.

    Args:
        data (list): A list containing note body and note tags.

    Returns:
        str: A confirmation message for the added note.
    """
    if len(data) == 0 :
        record_note = step_note_input()
    elif len(data) == 1:
        raise IndexError
    elif len(data)==2:
        note_body, note_tag, = data
        record_note = RecordNote(note_body, [note_tag])
    else:
        note_body = " ".join(filter(lambda x: not x.startswith("#"), data))
        list_tag = list(filter(lambda x: x.startswith("#"), data))
        if len(list_tag) == 0:
            raise IndexError
        record_note = RecordNote(note_body, list_tag)
    n_book.add_note_record(record_note)
    return f"Note {str(record_note)} has been added"


def step_note_input() -> RecordNote:
    """
    Prompt the user to enter note body and note tags step by step.

    Returns:
        RecordNote: A note record created from the entered information.
    """
    dict_input = {NoteBody: False, NoteTag: False}
    counter = 0
    while counter < len(dict_input):
        key_class = list(dict_input.keys())[counter]
        var_input = input(f"Enter {key_class.__name__.lower()}: ")

        if key_class.__name__ == "NoteTag":
            var_input = "#" + var_input if not var_input.startswith("#") else var_input
        try:
            dict_input[key_class] = key_class(var_input)
        except ValueError as er:
            print(er)
            continue
        counter += 1
    note_body, note_tag = dict_input.values()
    return RecordNote(note_body, [note_tag])

@input_error
def add_note_tag_handler(data : list[str]) -> str:
    """
    Add a new note tag to an existing note.

    Args:
        data (list): A list containing information about note.

    Returns:
        str: A confirmation message for the added note tag.
    """
    if len(data) <= 1 : raise IndexError
    note_id, new_tag, = data
    n_book[note_id].add_note_tag(new_tag)
    return f"Successful added tag {NoteTag(new_tag)} to note {str(n_book[note_id])}"

@input_error
def change_note_text_handler(data : list[str]) -> str:
    """
    """
    if len(data) < 1: raise IndexError
    note_id, new_text = data[0], data[1:]
    n_book[note_id].note_body = new_text
    return f"Note {str(n_book[note_id])} has been changed"

@input_error
def remove_note_tag_handler(data: list[str]) -> str:
    """
    Delete a note tag from an existing note.

    Args:
        data (list): A list containing note tag.

    Returns:
        str: A confirmation message for the deleted note tag.
    """
    if len(data) <= 1: raise IndexError
    note_id, note_tag, = data
    n_book[note_id].remove_note_tag(note_tag)
    return f"note tag - {NoteTag(note_tag)} has been deleted form your note {str(n_book[note_id])}"

@input_error
def delete_note_handler(data: list[str]) -> str:
    """
    Delete an existing note.

    Args:
        data (list): A list containing note information.

    Returns:
        str: A confirmation message for the deleted note.
    """
    if len(data) < 1 : raise IndexError
    note_id, = data
    body = n_book[note_id].note_body
    del n_book[note_id] 
    return f"note '{body}' has been deleted"

@input_error
def find_note_for_id_handler(data: list[str]) -> str:
    """
        Search for notes by a given ID.

        Args:
            data (list): A list containing ID.

        Returns:
            str: A formatted list of notes matching the ID.
        """
    if len(data) < 1: raise IndexError
    note_id, = data
    return n_book[note_id]


@input_error
def find_note_record_tag_handler(data: list[str]) -> str:
    """
    Search for notes by a given keyword (note tags).

    Args:
        data (list): A list containing search keyword (note tag).

    Returns:
        str: A formatted list of notes matching the search keyword (note tag).
    """
    if len(data) < 1 : raise IndexError
    search_tag, = data
    find_notes = "\n".join([str(rec) for rec in n_book.find_note_record_tag(search_tag)])
    if not find_notes:
        return "any note tag was not found"
    return find_notes


@input_error
def show_note_by_page(data: list[str]) -> str:
    """
    Display notes page by page.

    Args:
        data (list): A list containing the number of records per page.

    Yields:
        str: Formatted notes for display, separated by pages.
    """
    count_record, = data if len(data) >= 1 else "1"
    try:
        count_record = int(count_record)
        yield "input any for next page"
        for i, page in enumerate(n_book.notes_iterator(count_record), 1):
            page = "\n".join(map(lambda x: str(x), page ))
            input("")
            head = f'{"-" * 15} Page {i} {"-" * 15}\n'
            yield head + page
        yield f'{"-" * 15} end {"-" * 15}\n'
    except ValueError: # без єтого гавнокода все падает(с вводом не цифр)
        for _ in range(1):
            yield "invalid input count page"

def help_note_handler(*args) -> str:
   return "\n".join(
        ['{:<26}{:<}'.format(" / ".join(com_anot[0]), com_anot[1])
        for com_anot in COMMANDS_HELP.values()
        ]
    )

def show_all_notes(*args) -> str:
    return n_book.output_all_data()


def start_handler(*args) -> str:
    return "How can I help you?"


def exit_note_handler(*args) -> str:
    with open(file_notes_json, "w") as file:
        json.dump(n_book, file, cls=BookEncoder, sort_keys=True, indent=4)
    return "\nNotes book has been closed\n"


def unknown_command(*args) -> str:
    return 'Unknown command'


def command_parser_notes(row_str: str):
    """
    Parse a row string to identify and extract a command and its arguments.

    Args:
        row_str (str): A string containing the command and its arguments.

    Returns:
        tuple: A tuple containing the identified command key and a list of arguments.
    """
    row_str = re.sub(r'\s+', ' ', row_str)
    elements = row_str.strip().split(" ")
    for key, value in BOT_NOTE_COMMANDS.items():
        if elements[0].lower() in value[0]:
            return key, elements[1:]
        elif " ".join(elements[:2]).lower() in value[0]:
            return key, elements[2:]
    return unknown_command, None


BOT_NOTE_COMMANDS = {
    start_handler: (
        ["start"],
        "start"
        ),
    add_note_record_handler: (
        ["add", "+"],
        "note text #tegs / step"
        ),
    add_note_tag_handler: (
        ["add tag"],
        "ID(note) #tag"
        ),
    change_note_text_handler :(
        ["change text", "change note", "change"],
        "ID(note) new text to note"
    ),    
    remove_note_tag_handler: (
        ["remove tag"],
        "tag ID(note) #tag"
        ),
    delete_note_handler: (
        ["delete"],
        "ID(note)"
        ),
    find_note_record_tag_handler: (
        ["find_tag"],
        "#tag - show all notes whith this #tag"
        ),
    find_note_record_tag_handler: (
        ["find"],
        "ID(note)"
        ),
    show_all_notes: (
        ["show all"],
        " - show all notes"
        ),
    show_note_by_page: (
        ["show page"],
        "int_num(positive) - show all notes by step"
        ),
    help_note_handler: (
        ["help"],
        " - show all bot commands"
        ),
    exit_note_handler: (
        ["menu", "back", "esc"],
        " - save changesets and go to menu"
        ),
}

COMMANDS_HELP = {k.__name__:v for k,v in BOT_NOTE_COMMANDS.items()}

Completer_nb = get_completer([tupl[0] for tupl in BOT_NOTE_COMMANDS.values()])

def main_notes():
    clear()
    print(help_note_handler())
    while True:
        user_input = prompt(
            message="\nNotes Book >>>",
            completer=Completer_nb,                
            lexer=RainbowLexer("#ff00ff")               
            )
        if not user_input or user_input.isspace():
            continue

        func_handler, data = command_parser_notes(user_input)

        if func_handler == show_note_by_page:
            for page in func_handler(data):
                print(page)
            continue

        bot_message = func_handler(data)
        print(bot_message)

        if func_handler == exit_note_handler:
            break


if __name__ == "__main__":
    main_notes()



