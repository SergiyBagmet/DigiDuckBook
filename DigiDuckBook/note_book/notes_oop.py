from collections import UserDict
import typing as t
import json

from DigiDuckBook.abc_book import AbstractData

class FieldNotes:
    """
    Class parent representing a field used in the record of the notes book.
    """
    def __init__(self, value: str) -> None:
        self.value = value

    def __valid_value(self, value) -> None:
        if not isinstance(value , str) :
            raise TypeError(f'Value {value} not correct, you should enter a string')
        
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


class NoteTag(FieldNotes):
    """
    Class representing the Note tag field in a record in the notes book.
    """
    def __note_tag_validation(self, note_tag: str) -> None:
        if not (2 <= len(note_tag) <= 20):
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
    def __note_body_validation(self, note_body: str) -> None:
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
            note_body :NoteBody | str, 
            note_tags: list[NoteTag] | list[str] = [],
            note_id: None = None, # for init out json
            ) -> None:
        
        self.note_id = str(self.unic_id(note_id)) 
        self.note_tags = [self._tag(note_tag) for note_tag in note_tags] 
        self.note_body = self._body(note_body)

    
    def unic_id(self, id) -> int:
        if id is None :
            __class__.counter += 1
            return self.counter
        else:
            return id

    
    def _tag(self, tag: str | NoteTag) -> NoteTag:
        if not isinstance(tag, NoteTag):
            tag = NoteTag(tag)
        return tag

    
    def _body(self, body: str | NoteBody) -> NoteBody:
        if not isinstance(body, NoteBody):
            body = NoteBody(body)
        return body    

    def add_note_tag(self, note_tag: NoteTag | str):
        """
        Add a new notetag to the list of notetag for the note.
        Args:
            notetag (Notetag) or try valid Str: The notetag is already added to the note.
        Returns:
            None: This method does not return any value.
        """ 
        if (note_tag := self._tag(note_tag)) in self.note_tags:
            raise ValueError("This notetag has already been added")
        self.note_tags.append(note_tag)

    def remove_note_tag(self, note_tag: NoteTag | str) -> None:
        """
        Remove a notetag from the list of notetag for the note.

        Args:
            notetag (Notetag) or try valid Str: The notetag to be removed from the note.
        Raises:
            ValueError: If the notetag is not found in the notetag's list of notetags.
        Returns: 
            None: This method does not return any value.
        """
        if (note_tag:=self._tag(note_tag)) not in self.note_tags:
            raise ValueError(f"The note tag '{note_tag}' is not in this notes book.")
        if len(self.note_tags) == 0:
            raise ValueError(f"I can't remove last tag, writhe 'delete {self.note_id}' to remove notes")
        self.note_tags.remove(note_tag)

    def __str__(self) -> str:   
        return (
            f'\n\tID: {self.note_id}\n'
            f'\tNote tags: {" ".join(map(str, self.note_tags))}\n'
            f'\t{self.note_body}\n')
    
    def to_dict(self) -> dict[int, dict[list[str], str]]:
        note_tags = [str(note_tag) for note_tag in self.note_tags]
        note_body = None if self.note_body is None else str(self.note_body)
        return {
            str(self.note_id): {
                "Tags": note_tags,
                "Note": note_body,
            },
        }

class NotesBook(UserDict, AbstractData):
    """
    A class representing an notes book, which is a dictionary 
    with note_id as keys and record notes objects as values.
    """
    def add_note_record(self, note_record: RecordNote):
        if not isinstance(note_record, RecordNote):
            raise TypeError("Note Record must be an instance of the RecordNote class.")
        self[note_record.note_id] = note_record
        RecordNote.counter = int(note_record.note_id) 
    

    def find_note_record_tag(self, tag: str) -> list[RecordNote]:
        list_rec_notes = []

        for rec_note in self.data.values():         
            if (tag := rec_note._tag(tag)) in rec_note.note_tags:
                list_rec_notes.append(rec_note)
        return list_rec_notes   
     
    def __getitem__(self, id: str) -> RecordNote:
        """
        Retrieve a record from the address book by its id.

        Args:
            id (str): The id of the record to retrieve.
        Returns:
            RecordNote: The record object corresponding to the given id.
        Raises:
            KeyError: If the provided name is not found in the note book.
        """
        record_note = self.data.get(id)
        if record_note is None:
            raise KeyError(f"This id {id} isn't in Note Book")
        return record_note

    def __setitem__(self, id: str, val: RecordNote) -> None:
        """
        Add or update a record in the address book.

        Args:
            id (str): The note_id of the record.
            val (RecordNote): The record_note object to be added or updated.
        Raises:
            TypeError: If the given id is not an instance of the RecordNote class.
            KeyError: If the provided name is already present in the note book.
        """
        if not isinstance(val, RecordNote):
            raise TypeError("Record must be an instance of the RecordNote class.")
        if id in self.data:
            raise KeyError(f"Note on this id'{id}' is already in notes")
        self.data[id] = val

    def __delaitem__(self, id: str) -> None:
        """
        Delete a record from the note book by its ID.

        Args:
            key (str): The name of the record to delete.
        Raises:
            KeyError: If the provided ID is not found in the note book.
        """
        if not isinstance(id, str):
            raise KeyError("Value must be string")
        if not id in self.data:
            raise KeyError(f"Can't delete note {id} isn't in note Book")
        del self.data[id]

    def __str__(self) -> str:
        return '\n'.join([str(r) for r in self.values()])
    
    def output_all_data(self) -> str:
        return "\n".join([str(record) for record in self.values()])

    def to_dict(self) -> dict:
        """
        Convert the notes book to a dictionary.

        Returns:
            dict: A dictionary representing the notes book.
        """
        res_dict = {}
        for note_record in self.data.values():
            res_dict.update(note_record.to_dict())
        return res_dict
    
    def from_dict(self, data_json: dict) -> None:
        """
        Load data from a dictionary into the notes book.

        Args:
            data_json (dict): A dictionary containing data for the address book.
        Raises:
            TypeError: If the provided data is not a dictionary.
        """
        if not isinstance(data_json, dict):
            raise TypeError("this is not dict")
        
        for key, value in data_json.items():
            self.add_note_record(
                RecordNote(note_id=key, note_tags=value['Tags'], note_body=value['Note'])
            )



    def notes_iterator(self, note_item_number: int) -> t.Generator[RecordNote, int, None]:
        """
        Iterate through the records in the notes book and yield groups of note records.

        Args:
            item_number (int) > 0: The number of note records to be yielded at a time.

        Yields:
            List[Record]: A list containing a group of note records.

        Notes:
            If the given item_number is greater than the total number of note records in the notes book,
            all records will be yielded in one group.

        """
        if note_item_number <= 0:
            raise ValueError("Item number must be greater than 0.")
        elif note_item_number > len(self.data):
            note_item_number = len(self.data)

        list_note_records = []
        for counter, note_record in enumerate(self.data.values(), 1):
            list_note_records.append(note_record)
            if (not counter % note_item_number) or counter == len(self.data):
                yield list_note_records
                list_note_records = []

if __name__ == "__main__":
    pass