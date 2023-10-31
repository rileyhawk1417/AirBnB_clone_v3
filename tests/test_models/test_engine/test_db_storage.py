#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}

pepErrMsg = "Found code style errors (and warnings)."
dbDocString = "DBStorage class needs a docstring"
dbPyDocString = "db_storage.py needs a docstring"
docString = "method needs a dosctring"


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/engine/db_storage.py"])
        self.assertEqual(result.total_errors, 0, pepErrMsg)

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            [
                "tests/test_models/test_engine/\
test_db_storage.py"
            ]
        )
        self.assertEqual(result.total_errors, 0, pepErrMsg)

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None, dbPyDocString)
        self.assertTrue(len(db_storage.__doc__) >= 1, dbPyDocString)

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None, dbDocString)
        self.assertTrue(len(DBStorage.__doc__) >= 1, dbDocString)

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(
                func[1].__doc__, None, "{:s} {}".format(func[0], docString)
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} {}".format(func[0], docString),
            )


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_get(self):
        """Test the get method"""
        obj = State(name="California")
        models.storage.new(obj)
        models.storage.save()
        fetched_obj = models.storage.get(State, obj.id)
        self.assertIsNotNone(fetched_obj)
        self.assertEqual(obj.id, fetched_obj.id)

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_count(self):
        """Test the count method"""
        first_count = models.storage.count(State)
        models.storage.new(State(name="Arizona"))
        models.storage.save()
        self.assertEqual(models.storage.count(State), first_count + 1)
