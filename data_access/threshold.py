from data_access.mongo_access import MongoCollectionAccess
from bson.objectid import ObjectId

THRESHOLD_COLLECTION_NAME = 'threshold'

class Threshold:
    def __init__(
            self,
            user_id,
            before,
            onehour_after,
            twohour_after,
            _id = None
        ):
        if not isinstance(user_id, ObjectId):
            raise ValueError(f"user_id must be an instance of ObjectId class")

        self._id = ObjectId() if _id is None else _id
        self.before = before
        self.onehour_after = onehour_after
        self.twohour_after = twohour_after
        self.user_id = user_id

    @staticmethod
    def from_dict(data):
        return Threshold(
            _id=data.get('_id'),
            before=data.get('before'),
            onehour_after=data.get('onehour_after'),
            twohour_after=data.get('twohour_after'),
            user_id=data.get('user_id')
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "before": self.before,
            "onehour_after": self.onehour_after,
            "twohour_after": self.twohour_after,
            "user_id": self.user_id
        }

class ThresholdInterface:
    def __init__(self, mongo_client_db, user_id, verbose=False):
        self.mongo_collection_access = MongoCollectionAccess(
            mongo_client_db,
            THRESHOLD_COLLECTION_NAME,
            verbose
        )
        result = self.mongo_collection_access.find_document({
            "user_id": user_id
        })
        if result:
            self.threshold = result
        else:
            raise ValueError(f"Threshold for user {user_id} not found")

    def check_glucose_level(self, key, checked_level):
        checked_key = key.split('.')[-1]
        checked_threshold = self.threshold.get(checked_key)
        result = "HIGH LEVEL!!!" if (checked_level >= checked_threshold) else "Normal Level."
        print(f"{result} Threshold is {checked_threshold}")