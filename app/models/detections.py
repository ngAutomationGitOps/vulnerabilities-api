from datetime import datetime
from app.utilities.mongo import get_db
  # assumes your Mongo utils return a collection

class Detection:
    db = get_db()
    collection = db["Detection"]
  

    def __init__(self, agent_id, vuln_id, detected_at, status="pending", resolved_at=""):
        self.agent_id = agent_id
        self.vuln_id = vuln_id
        self.detected_at = detected_at
        self.status = status
        self.resolved_at = resolved_at


  
    @staticmethod
    def from_excel_row(row):
        return Detection(
            agent_id=row['Agent ID'],
            vuln_id=row['Vuln ID'],
            detected_at=row['Detected At'],
            status = row['Status'],
            resolved_at = row['Resolved At']
        )

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "vuln_id": self.vuln_id,
            "detected_at": self.detected_at,
            "status": self.status,
            "resolved_at": self.resolved_at
        }


    def insert(self):
        return self.collection.insert_one(self.to_dict())

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
    def update_one(cls, query, update):
        return cls.collection.update_one(query, {"$set": update})

    @classmethod
    def insert_many(cls, docs):
        return cls.collection.insert_many(docs)
    
    @classmethod
    def count(cls, query={}):
        return cls.collection.count_documents(query)
