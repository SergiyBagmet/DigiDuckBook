import os, json
import typing as t


DIR_DATA = "data"
if not os.path.isdir(DIR_DATA): os.makedirs(DIR_DATA)


def get_obj(file_json: str, cls: t.Type[object]) -> t.Type[object]:
    """
    Deserialize an object from a JSON file and return an instance of the specified class.

    Args:
        file_json (str): The path to the JSON file to deserialize.
        cls (Type[object]): The class type used to instantiate the object.

    Returns:
        Type[object]: An instance of the specified class with data from the JSON file.

    Raises:
        TypeError: If the specified class does not have a 'from_dict' method required for deserialization.
    """
    if not hasattr(cls, "from_dict"): 
        raise TypeError("The specified class must have a 'from_dict' method for deserialization.")
    a_book = cls() 
    try:
        with open(file_json, "r") as file:
            unpacked = json.load(file)
        a_book.from_dict(unpacked)
    except FileNotFoundError:
        with open(file_json, "w") as file:
            json.dump({}, file)
    return a_book      
  
  
class BookEncoder(json.JSONEncoder):
    """
    Encoder class for serializing objects to JSON.

    The `default` method allows custom serialization of objects, including those
    that cannot be serialized using standard methods.

    Args:
        json.JSONEncoder: Class for serializing objects to JSON.
    """
    def default(self, obj: t.Type[object]) -> dict[str, str | list[str]] | t.Any:
        """
        Method that defines how to serialize an object to JSON.

        Args:
            obj (Type[object]): The object to be serialized. It should have a
                `to_dict` method to convert itself into a dictionary.

        Returns:
            dict[str, str | list[str]] | t.Any: A dictionary or value that
            represents the object in JSON format.
        """
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj) 