from data_access.mongo_access import MongoCollectionAccess
from bson.objectid import ObjectId

USER_COLLECTION_NAME = 'users'

class User:
    def __init__(self, username, email, _id = None):
        self._id = ObjectId() if _id is None else _id
        self.username = username
        self.email = email
    
    @staticmethod
    def from_dict(data):
        return User(
            _id=data.get('_id'),
            username=data.get('username'),
            email=data.get('email')
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email
        }

class UserInterface:
    def __init__(self, mongo_client_db, username, verbose=False):
        self.mongo_collection_access = MongoCollectionAccess(
            mongo_client_db,
            USER_COLLECTION_NAME,
            verbose
        )
        result = self.mongo_collection_access.find_document({
            'username': username
        })
        if result:
            self.user = User.from_dict(result)
        else:
            raise ValueError(f"User {username} not found")