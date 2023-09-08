from collections import UserDict
import typing as t



class FieldNotes:
    """
    Class parent representing a field used in the record of the notes book.
    """
    def __init__(self, value: str) -> None:
        self.value = value

    def __valid_value(self, value) -> None:
        if isinstance(value , str) :
            raise TypeError(f'Value {value} not corect have to be str')
        
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value: str, validation: t.Callable | None = None) -> None:
        self.__valid_value(value)
        if validation is not None : validation(value)
        self._value = value
               
    def __str__(self) -> str:
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={self.value})'
    
    def __eq__(self, other) -> bool:
        if hasattr(other, "value"):
            value = other.value
        else:
            value = other
        return self.value == value



class NoteName(FieldNotes):
    """
    Class representing the Note name field in a record in the notes book.
    """
  
    def __note_name_validation(self, note_name: str) -> None:
        if not (1<= len(note_name) <= 20):
            raise ValueError("Note name is too short or long")

    @FieldNotes.value.setter
    def value(self, note_name: str) -> None:
        FieldNotes.value.fset(self, note_name, self.__note_name_validation)



class NoteTag(FieldNotes):
    """
    Class representing the Note tag field in a record in the notes book.
    """
    def __note_tag_validation(self, note_tag: str) -> None:
        if not (1 <= len(note_tag) <= 10):
            raise ValueError("Tag is too short or long")

    @FieldNotes.value.setter
    def value(self, note_tag: str) -> None:
        FieldNotes.value.fset(self, note_tag, self.__note_tag_validation)



class NoteBody(FieldNotes):
    """
    Class representing the Note body field in a record in the notes book.
    """
    def __note_body_validation(note_body: str) -> None:
        if not (1 <= len(note_body) <= 300):
            raise ValueError("Tag is too short or long")

    @FieldNotes.value.setter
    def value(self, note_body: str) -> None:
        FieldNotes.value.fset(self, note_body, self.__note_body_validation)



class RecordNote:
    """
     Class representing a record of a note in a notes book.

    Attributes:
        note_id (int): The unique identifier of the note.
        note_name (NoteName | str): The name of the note.
        note_body (NoteBody | str): The content of the note.
        note_tags (list[NoteTag] | list[str]): A list of tags associated with the note.
    """
    counter: int = 0

    def __init__(
            self,
            note_name: NoteName | str,
            note_body :NoteBody | str, 
            note_tags: list[NoteTag] | list[str] = [], 
        ) -> None:
        
        self.note_id = self.counter
        self.counter += 1
        self.note_name = note_name
        self.note_tags = [note_tag for note_tag in note_tags]
        self.note_body = note_body

    # TODO сделай такие три и инит прогони через них там где селф
    # для note_name note_body note_tag
    # а так вообще красава мелкие недочети я поправил 
    # продолжай в том же духе докстринги сразу єто найс!!! даже я так не пишу
    # def _name(self, name: str | Name) -> Name:
    #     if not isinstance(name, Name):
    #         name = Name(name)
    #     return name    

    def add_notetag(self, notetag: NoteTag | str):
        pass 

    def change_notebody(self, notebody: NoteBody | str):
        pass

    def delete_notebody(self, notebody: NoteBody | str):
        pass


class NotesBook(UserDict):
    pass
    