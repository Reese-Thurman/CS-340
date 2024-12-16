from operator import truediv

from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        # USER = 'aacuser'
        # PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32794
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        print("Connection Successful")

# Create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            result = self.database.animals.insert_one(data)    # Data should be dictionary
            if result.acknowledged:                            # If create method worked, return true
                return True                                    # otherwise, return false
            else:
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Read method to implement the R in CRUD.
    def read(self, data):
        if data is not None:

            if data == "water":
                results = list(self.database.animals.find({
                    "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
                    "sex_upon_outcome": "Intact Female",
                    "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
                }))

            elif data == "mountain":
                results = list(self.database.animals.find({
                    "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky",
                                      "Rottweiler"]},
                    "sex_upon_outcome": "Intact Male",
                    "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
                }))

            elif data == "disaster":
                results = list(self.database.animals.find({
                    "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound",
                                      "Doberman Pinsch", "Rottweiler"]},
                    "sex_upon_outcome": "Intact Male",
                    "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
                }))

            else:
                results = list(self.database.animals.find(data))    # Convert from cursor to list
                                                                    # Return the result - empty list if no
            return results                                          # documents found

        else:
            raise Exception("Nothing to query, because data parameter is empty")

# Update method to implement the U in CRUD.
    def update(self, filter_data, update_data):
        if filter_data and update_data:
            results = self.database.animals.update_many(filter_data, {"$set": update_data}) # Update entries in database
            return results.modified_count                                                   # Return the number of
                                                                                            # updated entries
        else:
            raise Exception("Nothing to query, because a data parameter is empty")

# Delete method to implement the D in CRUD.
    def delete(self, data):
        if data:
            results = self.database.animals.delete_many(data)       # Delete entry in database
            return results.deleted_count                            # Return the number of deleted entries

        else:
            raise Exception("Nothing to query, because data parameter is empty")
