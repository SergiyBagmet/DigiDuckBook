from collections import UserDict
import typing as t



class FieldNotes:
    """
    Class parent representing a field used in the record of the notes book.
    """
    def __init__(self, value: str) -> None:
        self.value = value

    def __valid_value(self, value) -> None:
        if not isinstance(value , str) :
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
            note_id: None = None,
            ) -> None:
        # исправил
        self.note_id = str(self.unic_id(note_id)) # ложу строку так как ти дальше по коду хочешь строку ключом вообще можно инт влом било переписивать
        self.note_tags = [self._tag(note_tag) for note_tag in note_tags] 
        self.note_body = self._body(note_body)

    # добавил
    def unic_id(self, id) -> int:
        if id is None :
            __class__.counter += 1
            return self.counter
        else:
            return id

    #добавил используй где необходимо дальше по коду
    def _tag(self, tag: str | NoteTag) -> NoteTag:
        if not isinstance(tag, NoteTag):
            tag = NoteTag(tag)
        return tag

    #добавил --//--
    def _body(self, body: str | NoteBody) -> NoteBody:
        if not isinstance(body, NoteBody):
            body = NoteBody(body)
        return body    

    def add_notetag(self, note_tag: NoteTag | str):
        """
        Add a new notetag to the list of notetag for the note.
        Args:
            notetag (Notetag) or try valid Str: The notetag is already added to the note.
        Returns:
            None: This method does not return any value.
        """ 
        if note_tag := self._tag(note_tag) in self.note_tags:
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
            self.note_tags.remove(self._tag(note_tag))
        except ValueError:
            raise ValueError(f"phone: {note_tag} not exists")


    def change_notebody(self, new_notebody: NoteBody | str):
        pass # не будет старого просто перезаписиваем 
                # а если такой же метод для тега то да нужно старий и новий

    def __str__(self) -> str:
        # вывод заметки
        return (
            f'\n\tID: {self.note_id}\n'
            f'\tNote tags: {" ".join(map(str,self.note_tags))}\n' # исправил
            f'\t{self.note_body}\n')
    
    def to_dict(self) -> dict[int, dict[list[str], str]]:
        pass

class NotesBook(UserDict):
    """
    A class representing an notes book, which is a dictionary 
    with note_id as keys and record notes objects as values.
    """
    def add_note_record(self, note_record: RecordNote):
        if not isinstance(note_record, RecordNote):
            raise # TODO напиши я уже устал спать хочу 23.41
        self.data[note_record.note_id] = note_record # исправил у id нет поля валуе

    # исправил можно переделать єтот на __getitem__ но и єтот не особо нуже 
    #єто все можно било сделать и в хедлере банальной проверкой на нан
    def find_note_record(self, key_note_id: str): 
        if note_record := self.data.get(key_note_id) is None:
            raise ValueError("There isn't such note")
        return note_record
    
    # исправил а точнее переделал
    def find_note_record_tag(self, tag: str) -> list[RecordNote]:
        list_rec_notes = []

        for rec_note in self.data.values(): # items или values а так ти просто по ключам бежишь!!!!        
            if (tag := RecordNote._tag(tag)) in rec_note.note_tags:
                list_rec_notes.append(rec_note)

        return list_rec_notes    

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
        if not key in self.data:
            raise KeyError(f"Can't delete note {key} isn't in note Book")
        del self.data[key]


if __name__ == "__main__":
    tag_1 = NoteTag("#inc")
    note_1 = NoteBody("hello I'm the first note")
    rec_1 = RecordNote(note_1,[tag_1])

    tag_2 = NoteTag("#digit")
    note_2 = NoteBody("hello I'm the second note")
    rec_2 = RecordNote(note_2, [tag_2])

    tag_3 = NoteTag("#letter")
    note_3 = NoteBody("hello I'm the third note")
    rec_3 = RecordNote(note_3, [tag_3])

    print(rec_1, rec_2, rec_3)
