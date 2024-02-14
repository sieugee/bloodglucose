from pymongo import MongoClient, ReturnDocument

class MongoDbAccess:
    def __init__(self, uri, database):
        self.client = MongoClient(uri)
        self.db = self.client[database]

    def test_connection(self):
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            print("MongoDB connection successful")
        except Exception as e:
            print("MongoDB connection unsuccessful")
            print(f"Exception: {e}")


class MongoCollectionAccess:
    def __init__(self, mongo_client_db, collection, verbose=False):
        if not isinstance(mongo_client_db, MongoDbAccess):
            raise ValueError(f"mongo_client_db for collection {collection} must be an instance of MongoDbAccess class")
        self.collection = mongo_client_db.db[collection]
        self.verbose = verbose

    def find_document(self, query_condition, return_id_only=False):
        if self.verbose:
            print(f"Find document with query {query_condition}")
        document = self.collection.find_one(query_condition)
        if document:
            if self.verbose :
                print(f"Found document: {document}")
            if return_id_only:
                return document['_id']
            else:
                return document
        else:
            if self.verbose :
                print(f"No document found with condition {query_condition}")
            return None

    def find_all(self, query_condition):
        if self.verbose:
            print(f"Find documents with query {query_condition}")
        docs = self.collection.find(query_condition)
        return list(docs)

    def find_document_and_update(self, query_condition, new_values):
        if self.verbose:
            print(f"Find document with query {query_condition}")
        result = self.collection.find_one_and_update(
            query_condition,
            {'$set': new_values},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        if self.verbose:
            print(f"The updated document is: {result}")
        return result
