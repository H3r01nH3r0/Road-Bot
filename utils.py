from json import load, dump
from io import BytesIO


def get_config(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as file:
        data: dict = load(file)
    return data



def save_config(filename: str, data: dict) -> None:
    for key in data.keys():
        if len(key) == 2:
            del data[key]

    with open(filename, "w", encoding="utf-8") as file:
        dump(data, file, indent=4, ensure_ascii=False)
