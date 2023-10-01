from abc import ABC, abstractmethod
import typing as t



class Field(ABC):
    """
    Parent class representing a field used in the record of the address book.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    @abstractmethod
    def _valid_value(self, value) -> None:
        pass
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str, validation: t.Callable | None = None) -> None:
        if validation is not None:
            value = validation(value)
        self._value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"

    def __eq__(self, val):  # ==
        if isinstance(val, self.__class__):  # можно и через if hasattr(val, 'value'):
            val = val.value
        return self.value == val
    

# class Record(ABC): 
# TODO сделать абстрактную запись(Record) 
# переименовать класс рекорд в рекорд_аб или подобний по смислу

   
class Updater(ABC):
    
    @abstractmethod
    def execute_to(self, record: object):
        pass
    
    @abstractmethod
    def info(self):
        pass
     
class UserDictCRUD(ABC):
      
    @abstractmethod
    def create(self, record: object):
        pass
    
    @abstractmethod
    def read(self, key: str):
        pass
    
    @abstractmethod
    def update(self, key: str, updater: Updater):
        pass
    
    @abstractmethod
    def delete(self, key: str):
        pass    
    
class AbstractBook(ABC):
    
    @abstractmethod
    def to_dict() -> dict:
        pass
    
    @abstractmethod
    def from_dict() -> None:
        pass
    
    @abstractmethod
    def show_all_data() -> t.Any:
        pass     