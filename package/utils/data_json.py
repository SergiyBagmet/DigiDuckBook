import os, json
import typing as t
DIR_DATA = "data"
if not os.path.isdir(DIR_DATA): os.makedirs(DIR_DATA)


def get_obj(file_json: str, cls: t.Type[object]) -> t.Type[object]:
    a_book = cls() 
    try:
        with open(file_json, "r") as file:
            unpacked = json.load(file)
        a_book.from_dict(unpacked)
    except FileNotFoundError:
        with open(file_json, "w") as file:
            json.dump({}, file)
    return a_book      
  