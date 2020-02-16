#!/usr/bin/env python3
# Author: Jhonatan Arenas <1164@holbertonschool.com>
# models/engine/file_storage.py
"""This module contains the engine of persistence"""
import json
from models.base_model import BaseModel


class FileStorage():
    """FileStorage contains the engines to persist the data"""

    __instances = 1

    def __init__(self):
        """
        Init method of thf FileStorage
        """
        if FileStorage.__instances:
            self.__file_path = 'file.json'
            self.__objects = dict()
            FileStorage.__instances -= 1

    def all(self):
        """
        Returns the objects saved
        """
        return self.__objects

    def new(self, obj):
        """
        Set in in the __objects attribute the obj with key: <obj class name>.id
        """
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        objects_copy = self.__objects
        json_dict = {key: objects_copy[key].to_dict() for key in objects_copy}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(json_dict, file, ensure_ascii=False)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exist; otherwise, do nothing)
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                load = json.load(file)
                for obj in load.values():
                    class_name = obj['__class__']
                    instance = eval(class_name)(**obj)
                    self.new(instance)
        except Exception:
            pass
