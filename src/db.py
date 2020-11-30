from pymongo import MongoClient
import json

class Database:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client["cmail"]
        self.collection = db["mail"]
    
    def create(self, to, subject, message):
        try :
            data = { "to": to, "subject": subject, "message": message }
            self.collection.insert_one(data)
            return True

        except Exception as e:
            return False

    def sent(self, page = 1, limit = 10):
        output = []
        data = list(self.collection.find().skip((page - 1) * limit).limit(limit))
   
        for o in data:
            obj = {}
            obj["id"] = str(o["_id"])
            obj["to"] = o["to"]
            obj["subject"] = o["subject"]
            obj["body"] = o["message"]

            print(obj)
            output.append(obj)
        
        return output