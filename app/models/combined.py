from datetime import datetime
from app.utilities.mongo import get_db
  # assumes your Mongo utils return a collection

class Combined:
    db = get_db()
    collection = db["vuln_enriched"]
    
    
  

    def __init__(self, agent_id, vuln_id, detected_at,  severity , cve_id , host , status="pending", resolved_at="",):
        self.agent_id = agent_id
        self.vuln_id = vuln_id
        self.detected_at = detected_at
        self.status = status
        self.resolved_at = resolved_at
        self.severity = severity
        self.cve_id = cve_id
        self.host = host
        


  
    @staticmethod
    def from_excel_row(row):
        return Combined(
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
        return cls.collection.estimated_document_count(query)
    
    @classmethod
    def count_by_status(cls, query={}):
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        result = cls.collection.aggregate(pipeline)
        return {doc["_id"]: doc["count"] for doc in result}


    @classmethod
    def get_severity_summary_by_owner(cls):
        pipeline = [
            { "$match": { "status": "pending" } },
            {
                "$lookup": {
                    "from": "agents_temp",
                    "localField": "agent_id",
                    "foreignField": "_id",
                    "as": "agent"
                }
            },
            { "$unwind": "$agent" },
            {
                "$group": {
                    "_id": {
                        "owner": "$agent.ServerDetail.Server_owner",
                        "severity": "$severity"
                    },
                    "count": { "$sum": 1 }
                }
            },
            {
                "$group": {
                    "_id": "$_id.owner",
                    "severities": {
                        "$push": {
                            "severity": "$_id.severity",
                            "count": "$count"
                        }
                    },
                    "total": { "$sum": "$count" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "owner": "$_id",
                    "severities": 1,
                    "total": 1
                }
            }
        ]

        result = list(cls.collection.aggregate(pipeline, allowDiskUse=True))
        print("Final result:", result)
        return result
    
    @classmethod
    def get_vuln_count_by_severity(cls, severity_level: str):
        pipeline = [
            {
                "$match": {
                    "status": "pending",
                    "severity": severity_level
                }
            },
            {
                "$count": "count"
            }
        ]

        print("Optimized pipeline:", pipeline)

        result = list(cls.collection.aggregate(pipeline, allowDiskUse=True))
        print("Final result:", result)

        return result[0] if result else { "count": 0 }