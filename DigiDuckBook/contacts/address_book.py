from collections import UserDict
import re
from datetime import date
import typing as t

from abc_class.abc_book import *
from calc_date import CalculateDate


class Name(Field):
    """
    Class representing the name field in a record of the address book.
    """
    def _valid_value(self, value) -> str:
        if not (len(value) > 2):
            raise ValueError(f'Name "{value}" is too short!')
        return value

    @Field.value.setter  # переопределяем сеттер родительского класса
    def value(self, value: str) -> None:
        Field.value.fset(self, value, self._valid_value)


class Phone(Field):
    """
    Class representing the phone field in a record of the address book.
    """ 
    def _valid_value(self, value) -> str:
        """
        Validate and format a phone number string.

        Args:
            value (str): The input phone number string to be validated.
        Returns:
            str: The validated and formatted phone number in the "+380xxxxxxxxx" format.
        Raises:
            ValueError: If the input value is not in the correct format.
        Example:
            valid_phone = __valid_phone("+380 (67) 123-45-67")
        """
        value = re.sub(r'[ \(\)\-]', '', value)
        phone_pattern = re.compile(r'\+380\d{9}|380\d{9}|80\d{9}|0\d{9}')
        if re.fullmatch(phone_pattern, value) is None:
            raise ValueError(f'Value {value} is not in correct format! Enter phone in format "+380xx3456789"')
        return f"+380{value[-9:]}"

    @Field.value.setter  # переопределяем сеттер родительского класса
    def value(self, value: str) -> None:
        Field.value.fset(self, value, self._valid_value)


class Email(Field):
    """
    Class representing the email field in a record of the address book.
    """

    def _valid_value(self, value: str) -> str:
        """
        Validate the correct format of email in the input email string.
        Valid format of email: (username)@(domainname).(top-leveldomain).
        Args:
            value (str): The input email string.
        Raises:
            ValueError: If the input email string is not in a valid format.
        Returns:
            str: The valid email string.
        """
        email_pattern = re.compile(r'[a-zA-Z]{1}[\S.]+@[a-zA-Z]+\.[a-zA-Z]{2,}') 
        # або r"[a-zA-Z0-9._ %-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2, }"
        if re.fullmatch(email_pattern, value) is None:
            raise ValueError(f'Value {value} is not in correct format! Enter it in format "email prefix @ email domain"')
        return value
        
    @Field.value.setter
    def value(self, value: str) -> None:
        Field.value.fset(self, value, self._valid_value)


class Birthday(Field):
    """
    Class representing the birthday field in a record of the address book.
    The date is stored in ISO 8601 format.
    """

    def _valid_value(self, value: str) -> str:
        """
        Input date string to a valid ISO-formatted date.
        Args:
            value (str): The input date string.
        Raises:
            ValueError: If the input date string is not in a valid date format(ISO).
        Returns:
            str: The valid ISO-formatted date string.
        """
        try:
            b_day = date.fromisoformat(value)
        except ValueError: 
            raise ValueError(f'Birthday {value} is not correct format! for example "2023-12-30"') 
        if b_day.year > date.today().year:
            raise ValueError(f'{value} -  you from the future?')
        return value    
    
    @Field.value.setter
    def value(self, value: str) -> None:
        Field.value.fset(self, value, self._valid_value)

    def get_date(self) -> date:
        return date.fromisoformat(self.value)


class Address(Field):
    """
    Class representing the address field in a record of the address book.
    """

    def _valid_value(self, value: str) -> str:
        """
        Validate the length of address in the input address string.
        Args:
            value (str): The input address string.
        Raises:
            ValueError: If the input address string exceeds the allowed length.
        Returns:
            str: The valid address string.
        """
        if value.isspace():
            raise ValueError(f'Address "{value}" is not in correct format!')
        if not (5 <= len(value) <= 50):
            raise ValueError(
                f'Address "{value}" is not in correct format! It must contain from 5 to 50 characters')
        return value

    @Field.value.setter
    def value(self, value: str) -> None:
        Field.value.fset(self, value, self._valid_value)



class Record(AbstractRecord):
    """
    Class representing a record in an address book.

    Attributes:
        name (Name): The name of the contact.
        phones (list): A list of phone numbers associated with the contact.
        email (Email): The email of the contact.
        birthday (Birthday): The birthday of the contact.
        address (Address): The address of the contact.
    """
    def __init__(
            self, 
            name: Name | str, 
            phones: list[Phone | str],
            email: Email | str| None = None,
            birthday: Birthday | str | None = None,
            address: Address | str | None = None,
        ) -> None:

        self.name = name
        self.phones = [phone for phone in phones]
        self.email = None if email is None else email
        self.birthday = None if birthday is None else birthday
        self.address = None if address is None else address
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name: Name | str ):
        if not isinstance(new_name, Name):
            new_name = Name(new_name)
        self._name = new_name
        
    @property
    def phones(self):
        return self._phones

    @phones.setter
    def phones(self, phones: list[Phone | str]):
        if not all(isinstance(ph, (Phone, str)) for ph in phones):
            raise ValueError("All elements in 'phones' list must be of type 'Phone' or 'str'.")
        phones = [Phone(ph) if isinstance(ph, str) else ph for ph in phones] 
        self._phones = phones
     
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, new_email: Email | str | None):
        if not isinstance(new_email, Email) and new_email is not None :
            new_email = Email(new_email)
        self._email = new_email
        
    @property
    def birthday(self):
        return self._birthday
    
    @birthday.setter
    def birthday(self, new_birthday: Birthday | str | None ):
        if not isinstance(new_birthday, Birthday) and new_birthday is not None:
            new_birthday = Birthday(new_birthday)
        self._birthday = new_birthday
        
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, new_address: Address | str | None):
        if not isinstance(new_address, Address) and new_address is not None:
            new_address = Address(new_address)
        self._address = new_address            
        

    def __str__(self) -> str:
        # вывод телефонов с новой строки и табуляцией
        birthday_str = f'birthday: {self.birthday or "Empty"}'
        email_str = f'email: {self.email or "Empty"}'
        address_str = f'address: {self.address or "Empty"}'
        phones_str = ", ".join([str(ph) for ph in self.phones])
        return (
            f'<Record>:\n\tname: {self.name}\n'
            f'\tphones: {phones_str or "Empty"}\n'
            f'\t{email_str}\n'
            f'\t{birthday_str}\n'
            f'\t{address_str}\n'
        )

    def get_date(self) -> date:
        if (b_day:= self.birthday) is None:
            raise ValueError(f"this contact '{self.name} has'nt birthday'")
        return b_day.get_date()
    
    def get_one_str(self) -> str:
        str_phones = " ".join(map(str, self.phones))
        return f'{self.name} {str_phones} {self.email} {self.birthday} {self.address}'.replace("None", "")

    def __repr__(self) -> str:
        return (
            f"Record(name={self.name!r}, "
            f'phones=[{", ".join([ph.__repr__() for ph in self.phones])}, '
            f'email={self.email!r}, '
            f'birthday={self.birthday!r},'
            f'address={self.address!r})'
        )

    def to_dict(self) -> dict[str, dict[str, list[str] | str | None]]:
        phones = [str(phone) for phone in self.phones]
        email = None if self.email is None else str(self.email)
        birthday = None if self.birthday is None else str(self.birthday)
        address = None if self.address is None else str(self.address)

        return {
            str(self.name): {
                "phones": phones,
                "email": email,
                "birthday": birthday,
                "address": address,
            },
        }


class Updaters:
# класс для удобства вибора вложених классов    
    class ChangeName(Updater):
        def __init__(self, new_name: Name | str) -> None:
            self.new_name = new_name
        
        def execute_to(self, record: Record) -> None:
            self.record = record
            self.old_name = record.name
            self.record.name = self.new_name
        
        
        def info(self) -> str:
            return f'contact name"{self.old_name}" has been changet to "{self.new_name}"'

    class AddPhone(Updater):
        def __init__(self, phone: Phone | str) -> None:
            self.phone = phone if isinstance(phone, Phone) else Phone(phone)
            
        def execute_to(self, record: Record) -> None:
            self.record = record
            if self.phone in self.record.phones:
                raise ValueError("this phone number has already been added")
            self.record.phones.append(self.phone)

        def info(self) -> str:
            return f'phone number {self.phone} has added at contact: {self.record.name}'

    class ChangePhone(Updater):
        def __init__(self, old_phone: Phone | str, new_phone: Phone | str ) -> None:
            
            self.old_phone = old_phone if isinstance(old_phone, Phone) else Phone(old_phone)
            self.new_phone = new_phone if isinstance(new_phone, Phone) else Phone(new_phone)
            
        def execute_to(self, record: Record) -> None: 
            self.record = record 
            if self.old_phone not in self.record.phones:
                raise ValueError(
                    f"The phone '{self.old_phone}' is not in this contact: '{self.record.name}'."
                )
            if self.new_phone in self.record.phones:
                raise ValueError(
                    f"The phone '{self.new_phone}' already in contact: '{self.record.name}'."
                )
            inx = self.record.phones.index(self.old_phone)
            self.record.phones[inx] = self.new_phone
        
        def info(self):
            return f'phone number {self.old_phone} has changed to {self.new_phone} at contact: {self.record.name}'

    class RemovePhone(Updater):
        def __init__(self, phone: Phone | str) -> None:
            self.phone = phone if isinstance(phone, Phone) else Phone(phone)
            
        def execute_to(self, record: Record) -> None:
            self.record = record
            if self.phone not in self.record.phones:
                raise ValueError(f"The phone '{self.phone}' is not in this record.")
            self.record.phones.remove(self.phone)
        
        def info(self) -> str:
            return f'phone number {self.phone} has removed at contact: {self.record.name}'

    class AddChangeEmail(Updater):
        def __init__(self, email: Email | str ) -> None:
            self.email = email
            
        def execute_to(self, record: Record) -> None:
            self.record = record
            self.record.email = self.email

        def info(self) -> str:
            return f'email {self.email} has added/changed at contact: {self.record.name}'    

    class RemoveEmail(Updater):
         
        def execute_to(self, record: Record) -> None:
            self.record = record
            self.email = self.record.email
            self.record.email = None
        
        def info(self) -> str:
            return f'email {self.email} has deleted at contact: {self.record.name}'
        
    class AddChangeBirthday(Updater):
        def __init__(self, birthday: Birthday | str) -> None:
            self.birthday = birthday
            
        def execute_to(self, record: Record) -> None:
            self.record = record
            self.record.birthday = self.birthday

        def info(self) -> str:
            return f'birthday {self.birthday} has added/changed at contact: {self.record.name}'    

    class RemoveBirthday(Updater):
         
        def execute_to(self, record: Record) -> None:
            self.record = record
            self.birthday = self.record.birthday
            self.record.birthday = None
        
        def info(self) -> str:
            return f'birthday {self.birthday} has deleted at contact: {self.record.name}'
        
    class AddChangeAddress(Updater):
        def __init__(self, address: Address | str ) -> None: 
            self.address = address
            
        def execute_to(self, record: Record) -> None:
            self.record = record
            self.record.address = self.address

        def info(self) -> str:
            return f'address {self.address} has added/changed at contact: {self.record.name}'    

    class RemoveAddress(Updater):
            
        def execute_to(self, record: Record) -> None:
            self.record = record
            self.address = self.record.address
            self.record.address = None
        
        def info(self) -> str:
            return f'address {self.address} has deleted at contact: {self.record.name}'    


class AddressBook(UserDict, AbstractBook):
    """
    A class representing an address book, which is a dictionary
    with record names as keys and record objects as values.
    """

    def to_dict(self) -> dict:
        """
        Convert the address book to a dictionary.

        Returns:
            dict: A dictionary representing the address book.
        """
        res_dict = {}
        for record in self.data.values():
            res_dict.update(record.to_dict())
        return res_dict

    def from_dict(self, data_json: dict) -> None:
        """
        Load data from a dictionary into the address book.

        Args:
            data_json (dict): A dictionary containing data for the address book.
        Raises:
            TypeError: If the provided data is not a dictionary.
        """
        if not isinstance(data_json, dict):
            raise TypeError("this is not dict")

        for name, record in data_json.items():
            AddressBookCRUD(self).create( # тут єто нормально? или по другому?
                Record(name=name, 
                       phones=record['phones'], 
                       email=record['email'], 
                       birthday=record['birthday'],
                       address=record['address']),
            ) #TODO сделать фромдикт в рекорде если добавляем новое поле там же и добавляем в методе?

    def __str__(self) -> str:
        return "\n".join([str(r) for r in self.values()])
    
    def get_dict_search(self) -> dict[str, Record]:
        return {r.get_one_str():r for r in self.data.values()}
 
class AddressBookCRUD(UserDictCRUD):
    
    def __init__(self, a_book: AddressBook) -> None:
        self.a_book = a_book 
        self.update_info: str | None = None
        
    def create(self, record: Record):
        if (key_name := record.name.value) in self.a_book.data:
            raise KeyError(f"This name '{key_name}' is already in contacts")
        self.a_book.data[key_name] = record
    
    def read(self, key_name: str) -> Record :
        record = self.a_book.data.get(key_name) 
        if record is None:
            raise KeyError(f"This name '{key_name}' isn't in Address Book")  
        return record
                  
    def update(self, key_name: str, updater: Updater) -> str:
        
        if (record := self.a_book.data.get(key_name)) is None:
            raise KeyError(f"This name {key_name} isn't in Address Book")
        
        updater.execute_to(record)
        match updater:
            case Updaters.ChangeName():
                self.delete(key_name)
                self.create(record)
        self.update_info = updater.info()
         
    def delete(self, key_name: str):
        if key_name not in self.a_book.data:
            raise KeyError(f"Can't delete contact '{key_name}' isn't in Address Book")
        del self.a_book.data[key_name]
    
    def show(self, 
             key_call: t.Literal["all", "page", "search", "days", "delta"], 
             arg_for_call: str | int=None
             ) -> str | t.Generator[Record, int, None]:
        
        show_ab = ShowAddressBook(self.a_book)
        match key_call:
            case "all":
                return "\n".join(map(lambda r: str(r)[9:], show_ab.show_all()))
            case "page":
                return show_ab.paginator(arg_for_call)
            case "search":
                return "\n".join(map(lambda r: str(r)[9:], show_ab.search(arg_for_call)))
            case "days":
                return str(CalculateDate.days_to_birthday(self.read(arg_for_call).get_date()))
            case "delta":
                rec_list = CalculateDate.find_obj_in_day_interval(list(self.a_book.values()), arg_for_call)
                return "\n".join(map(lambda r: str(r)[9:], rec_list))
            case _:
                raise KeyError(f'Invalid key: {key_call}. Expected one of ["all", "page", "search", "days", "delta"]')
                    

class ShowAddressBook:
    def __init__(self, a_book: AddressBook) -> None:
        self.a_book = a_book
    
    def show_all(self) -> list[Record]:
        return list(self.a_book.data.values())
     
    def paginator(self, item_number: int) -> t.Generator[Record, int, None]:

        if item_number <= 0:
            raise ValueError("Item number must be greater than 0.")
        elif item_number > len(self.a_book.data):  # если количство виводов(за раз) больше чем количество записей
            item_number = len(self.a_book.data)  # виводим все

        list_record = []
        for counter, record in enumerate(self.a_book.data.values(), 1):
            list_record.append(record)
            if (not counter % item_number) or counter == len(self.a_book.data):
                yield list_record
                list_record = []

    def search(self, search_word: str) -> list[Record]:
        search_list = []
        for str_val_record, record in self.a_book.get_dict_search().items():
            if search_word.lower() in str_val_record.lower():
                search_list.append(record)
        return search_list            
                

if __name__ == "__main__":
    pass
    

