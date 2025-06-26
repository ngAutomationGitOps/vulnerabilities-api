from datetime import datetime
from app.utilities.mongo import get_db

class Agent:
    db = get_db()
    collection = db["agents"]
    
    def __init__(self, _id, name, status, ip_address, os_name, os_platform, os_version, agent_version, group, registration_date):
        self._id = _id
        self.name = name
        self.status = status
        self.ip_address = ip_address
        self.os_name = os_name
        self.os_platform = os_platform
        self.os_version = os_version
        self.agent_version = agent_version
        self.group = group
        self.registration_date = registration_date
        self.vulnerabilities = []

    @staticmethod
    def from_excel_row(row):
        return Agent(
            _id=int(row['ID']),
            name=row['Name'],
            status=row['Status'],
            ip_address=row['IP address'],
            os_name=row['OS name'],
            os_platform=row['OS platform'],
            os_version=row['OS version'],
            agent_version=row['Version'],
            group=eval(row['Group']),
            registration_date=datetime.fromisoformat(row['Registration date'].replace('Z', ''))
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "status": self.status,
            "ip_address": self.ip_address,
            "Os": {
                "name": self.os_name,
                "platform": self.os_platform,
                "version": self.os_version
            },
            "agent_version": self.agent_version,
            "group": self.group,
            "registration_date": self.registration_date,
            "vulnerabilities": self.vulnerabilities
        }


    

    def insert(self):
        return self.collection.insert_one(self.to_dict())

    @classmethod
    def insert_many(cls, docs):
        return cls.collection.insert_many(docs)
    
    @classmethod
    def get_one(cls, query):
        return cls.collection.find_one(query)

    @classmethod
    def get_all(cls, query={}):
        return list(cls.collection.find(query))

    @classmethod
    def delete_one(cls, query):
        return cls.collection.delete_one(query)

    @classmethod
    def delete_many(cls, query):
        return cls.collection.delete_many(query)
    
    @classmethod
    def delete_all(cls, confirm=False):
        if confirm:
            return cls.collection.delete_many({})
        else:
            raise ValueError("Set confirm=True to delete all documents")

    
    @classmethod
    def update_one(cls, query, update):
        return cls.collection.update_one(query, {"$set": update})
    
    @classmethod
    def count(cls, query={}):
        return cls.collection.count_documents(query)