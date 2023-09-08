from collections import UserDict

class FieldNotes:
    """
    Class parent representing a field used in the record of the notes book.
    """
    def __init__(self, value: str) -> None:
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        try:
            self._value = value
        except TypeError:
            raise TypeError(f'Value {value} is not valid. Must be string')
    
    def __str__(self) -> str:
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={self.value})'
    
    def __eq__(self, other):
        if hasattr(other, "value"):
            value = other.value
        else:
            value = other
        return self.value == value

class NoteName(FieldNotes):
    """
    Class representing the Note name field in a record in the notes book.
    """
     @staticmethod
    def note_name_validation(notename: str) -> None:
        if not isinstance(notename, str):
            raise ValueError("Note name have to be str")
        if 1 >= len(notename) <= 20:
            raise ValueError("Note name is too short or long")

    @FieldNotes.value.setter
    def value(self, notename: str) -> None:
        self.note_name_validation(notename)
        FieldNotes.value.fset(self, notename)

class NoteTag(FieldNotes):
    """
    Class representing the Note tag field in a record in the notes book.
    """
     @staticmethod
    def note_tag_validation(notetag: str) -> None:
        if not isinstance(notetag, str):
            raise ValueError("Note tag have to be str")
        if 1 >= len(notetag) <= 20:
            raise ValueError("Tag is too short or long")

    @FieldNotes.value.setter
    def value(self, notetag: str) -> None:
        self.note_tag_validation(notetag)
        FieldNotes.value.fset(self, notetag)

class NoteBody(FieldNotes):
    """
    Class representing the Note body field in a record in the notes book.
    """
     @staticmethod
    def note_body_validation(notebody: str) -> None:
        if not isinstance(notebody, str):
            raise ValueError("Note body have to be str")
        if 1 >= len(notebody) <= 300:
            raise ValueError("Tag is too short or long")

    @FieldNotes.value.setter
    def value(self, notebody: str) -> None:
        self.note_body_validation(notebody)
        FieldNotes.value.fset(self, notebody)

class RecordNote:
    """
    Class representing a record of the note in an notes book.

    Attributes:
        ID - unic number of each note
        notename (Notename): The name of the note.
        tags (list): A list of tags associated with the contact.
        notebody (NoteBody): The note body
    """
    def __init__(
            self,
            id: int,
            notename: NoteName | str, 
            notetags: list[NoteTag] | list[str] = [], 
            notebody: NoteBody | str 
        ):
        
        self.id = id
        self.notename = notename
        self.notetags = [notetag for notetag in notetags]
        self.notebody = notebody

    def add_notetag(self, notetag: NoteTag | str):
        pass 

    def change_notebody(self, notebody: NoteBody | str):
        pass

    def delete_notebody(self, notebody: NoteBody | str):
        pass


class NotesBook:
