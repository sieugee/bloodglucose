from data_access.mongo_access import MongoCollectionAccess
from bson.objectid import ObjectId
from datetime import datetime

DAILY_LEVELS_COLLECTION_NAME = 'daily_levels'

class DailyLevels:
    def __init__(
            self,
            user_id,
            _id=None,
            date=None,
            morning=None,
            evening=None
        ):
        if not isinstance(user_id, ObjectId):
            raise ValueError(f"user_id must be an instance of ObjectId class")

        self._id = ObjectId() if _id is None else _id
        self.date = datetime.now() if date is None else date
        self.morning = morning if morning is not None else {"before": None, "onehour_after": None, "twohour_after": None}
        self.evening = evening if evening is not None else {"before": None, "onehour_after": None, "twohour_after": None}
        self.user_id = user_id

    @staticmethod
    def from_dict(data):
        return DailyLevels(
            _id=data.get('_id'),
            date=data.get('date'),
            morning=data.get('morning'),
            evening=data.get('evening')
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "date": self.date,
            "morning": self.morning,
            "evening": self.evening
        }

class DailyLevelsInterface:
    def __init__(self, mongo_client_db, user_id, verbose=False):
        self.mongo_collection_access = MongoCollectionAccess(
            mongo_client_db,
            DAILY_LEVELS_COLLECTION_NAME,
            verbose
        )
        self.user_id = user_id
        self.verbose = verbose

    def getAllGlucoseData(self):
        result_list = self.mongo_collection_access.find_all({
            "user_id": self.user_id
        })
        return result_list

    def find_document_by_date(self, searchdate):
        searchdatetime = datetime(
            searchdate.year,
            searchdate.month,
            searchdate.day
        )
        result = self.mongo_collection_access.find_document({
            "user_id": self.user_id,
            "date": searchdatetime
        }, True)
        if result:
            return result
        else:
            return None

    def update_glucose_level(self, date, key, new_value):
        if self.verbose:
            print('==========')
            print("Use the following input to update glucose level: ")
            print(date)
            print(key)
            print(new_value)
            print('==========')
        searchdatetime = datetime(date.year, date.month, date.day)
        result = self.mongo_collection_access.find_document_and_update(
            {
                "user_id": self.user_id,
                "date": searchdatetime
            },
            {
                key: new_value
            }
        )
        return result

