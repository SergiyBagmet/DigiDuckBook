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



# class NoteName(FieldNotes):
    # """
    # Class representing the Note name field in a record in the notes book.
    # """
  
    # def __note_name_validation(self, note_name: str) -> None:
    #     if not (1<= len(note_name) <= 20):
    #         raise ValueError("Note name is too short or long")

    # @FieldNotes.value.setter
    # def value(self, note_name: str) -> None:
    #     FieldNotes.value.fset(self, note_name, self.__note_name_validation)



class NoteTag(FieldNotes):
    """
    Class representing the Note tag field in a record in the notes book.
    """
    def __note_tag_validation(self, note_tag: str) -> None:
        if not (2 <= len(note_tag) <= 10):
            raise ValueError("Tag is too short or long")
        if not note_tag.startswith('#'):
            raise ValueError("Tag should start with #")


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
            # note_name: NoteName | str,
            note_body :NoteBody | str, 
            note_id: None,
            note_tags: list[NoteTag] | list[str] = [],
            ) -> None:
        
        self.note_id = self.counter if note_id is None else note_id
        self.counter += 1
        # self.note_name = note_name
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

    def add_notetag(self, note_tag: NoteTag | str):
        """
        Add a new notetag to the list of notetag for the note.
        Args:
            notetag (Notetag) or try valid Str: The notetag is already added to the note.
        Returns:
            None: This method does not return any value.
        """ 
        if note_tag in self.note_tags:
            raise ValueError("This notetag has already been added")
        self.note_tags.append(note_tag)

    def remove_notetag(self, note_tag: NoteTag | str) -> None:
        """
        Remove a notetag from the list of notetag for the note.

        Args:
            notetag (Notetag) or try valid Str: The notetag to be removed from the note.
        Raises:
            ValueError: If the notetag is not found in the notetag's list of notetags.
        Returns: 
            None: This method does not return any value.
        """
        try:
            self.note_tags.remove(note_tag)
        except ValueError:
            raise ValueError(f"phone: {note_tag} not exists")


    def change_notebody(self, old_notebody: NoteBody | str, new_notebody: NoteBody | str):
        pass

    def __str__(self) -> str:
        # вывод заметки
        return (
            f'<Record>:\n\tID: {self.note_id}'
            f'\n\tNote tags: {self.note_tags}\n\t'
            f'{self.note_body}\n')
    
    def to_dict_note_records(self) -> dict[int, dict[list[str], str]]:
        pass

class NotesBook(UserDict):
    """
    A class representing an notes book, which is a dictionary 
    with note_id as keys and record notes objects as values.
    """
    def add_note_record(self, note_record: RecordNote):
        self.data[note_record.note_id.value] = note_record

    def find_note_record(self, key_note_id: str):
        result = self.data.get(key_note_id)
        if self.data.get(key_note_id) == None:
            raise ValueError("There isn't such note")
        return result
    
    def find_note_record_tag(self, tag: str):
        results = []

        for key, value in self.data():
            inner_list, result = value
            if tag in inner_list:
                results.append((key, result))
            else:
                raise ValueError("There isn't such note")

    def __delaitem__(self, key: str) -> None:
        """
        Delete a record from the note book by its ID.

        Args:
            key (str): The name of the record to delete.
        Raises:
            KeyError: If the provided ID is not found in the note book.
        """
        if not isinstance(key, str):
            raise KeyError("Value must be string")
        if key not in self.data:
            raise KeyError(f"Can't delete note {key} isn't in note Book")
        del self.data[key]


if __name__ == "__main__":
    tag_1 = NoteTag("#inc")
    note_1 = NoteBody("hello I'm the first note")
    # rec_1 = RecordNote(tag_1, note_1)

    # tag_2 = NoteTag("#digit")
    # note_2 = NoteBody("hello I'm the second note")
    # rec_2 = RecordNote(tag_2, note_2)

    # tag_3 = NoteTag("#letter")
    # note_3 = NoteBody("hello I'm the third note")
    # rec_3 = RecordNote(tag_3, note_3)

