import copy
import logging
from datetime import datetime, timezone

from bson import ObjectId
from errors.handling_errors import (
    CollectionNameEmpty,
    DefaultError,
    ValueDontExists,
)
from utils.constants import DELETE_NOT_ALLOW

logger = logging.getLogger(__name__)


class BaseManager:
    COLLECTION_NAME = None

    @classmethod
    def validate_collection_name(cls):
        """Validate exists collection name"""
        if not cls.COLLECTION_NAME:
            raise CollectionNameEmpty

    @classmethod
    def get_collection(cls):
        """Get Collection"""
        from main import db

        cls.validate_collection_name()
        return db.get_collection(cls.COLLECTION_NAME)

    @classmethod
    def get_by_id(cls, value_id: str):
        """Get single objects
        params:
            value_id(str): Value ID
        """
        collection = cls.get_collection()
        try:
            value = collection.find_one({"_id": ObjectId(value_id)})
        except Exception:
            raise ValueDontExists

        # In case of being an empty value,
        # we execute a raise error,
        # I say that the value does not exist
        if not value:
            raise ValueDontExists
        return value

    @classmethod
    def filter_values(cls, query: dict = None):
        """Filter values by query"""
        collection = cls.get_collection()
        data_query = copy.deepcopy(query) or {}
        try:
            values = collection.find(data_query)
        except Exception:
            values = []

        return values

    @classmethod
    def get_one(cls, values: dict):
        """Get single objects
        params:
            value_id(str): Value ID
        """
        collection = cls.get_collection()
        try:
            value = collection.find_one(values)
        except Exception:
            raise ValueDontExists
        return value

    @classmethod
    def get_with_or(cls, values: list):
        """Get single object filtered by one value or other
        :params values: Dict (header - value) to filter
        """
        collection = cls.get_collection()
        try:
            value = collection.find_one({"$or": values})
        except Exception:
            raise ValueDontExists
        return value

    @classmethod
    def filter_list_values(cls, key, query):
        """Filter values by query"""
        collection = cls.get_collection()
        try:
            values = collection.find({key: {"$in": query}})
        except Exception:
            values = []
        return values

    @classmethod
    def update_value_by_id(cls, value_id: str, data):
        """Update document by ID
        params:
            value_id(str): Value ID
        """
        collection = cls.get_collection()
        cls.get_by_id(value_id)
        update_data = copy.deepcopy(data) or {}
        now = datetime.now(timezone.utc)
        if update_data:
            update_data["updated_at"] = now
        try:
            value = collection.update_one(
                {"_id": ObjectId(value_id)}, {"$set": data}
            )
        except Exception as error:
            raise DefaultError(str(error))

        return value

    @classmethod
    def delete_by_id(cls, value_id: str):
        """Remove document by ID
        params:
            value_id(str): Value ID
        """
        collection = cls.get_collection()
        cls.get_by_id(value_id)
        try:
            collection.delete_one({"_id": ObjectId(value_id)})
        except Exception as error:
            raise DefaultError(str(error))

    @classmethod
    def delete_many(cls, values: dict):
        """Delete values by query"""
        collection = cls.get_collection()
        try:
            if values:
                value = collection.delete_many(values)
            else:
                raise Exception(DELETE_NOT_ALLOW)
        except Exception as err:
            return err
        return value

    @classmethod
    def insert_one(cls, data: dict = None):
        """Insert single value
        params:
            data(dict): Data to create document.
        """
        data_insert = copy.deepcopy(data) or {}
        now = datetime.now(timezone.utc)
        if data_insert:
            data_insert["created_at"] = now
            data_insert["updated_at"] = now
        collection = cls.get_collection()
        try:
            value = collection.insert_one(data_insert)
        except Exception as error:
            raise DefaultError(str(error))

        return value

    @classmethod
    def remove(cls, query: str = None):
        """Remove data from collection"""
        collection = cls.get_collection()
        data_insert = copy.deepcopy(query) or {}
        try:
            collection.delete_one(**data_insert)
        except Exception as error:
            raise DefaultError(str(error))

    @classmethod
    def update_value_update_many(cls, query: str = None, data: dict = None):
        """Update data from collection"""
        collection = cls.get_collection()
        query_filter = copy.deepcopy(query) or {}
        update_data = copy.deepcopy(data) or {}
        now = datetime.now(timezone.utc)
        if update_data:
            update_data["updated_at"] = now
        try:
            value = collection.update_one(query_filter, update_data)
        except Exception as error:
            raise DefaultError(str(error))

        return value

    @classmethod
    def find_one_and_update(
        cls,
        _id,
        update_value,
    ):
        """Filter value and update the data from collection"""
        collection = cls.get_collection()
        try:
            value = collection.find_one_and_update(
                **{
                    "filter": {"_id": _id},
                    "update": {"$setOnInsert": update_value},
                    "new": True,  # return new doc if one is upserted
                    "upsert": True,  # insert the document if it does not exist
                }
            )
        except Exception as error:
            raise DefaultError(str(error))
        return value
