from datetime import datetime
from app.utilities.mongo import get_db
from app.helpers.dateFormatHandler import parse_detected_at


class Vulnerability:
    db = get_db()
    collection = db["Vulnerabilities"]
    collection_temp = db["Vulnerabilities_temp"]
    

    def __init__(self, cve_id, severity, description, os_name, os_platform, os_full,
                 package_name, package_version, package_type,
                 reference, remediation, detected_at=None):
        self.cve_id = cve_id
        self.severity = severity
        self.description = description
        self.os_name = os_name
        self.os_platform = os_platform
        self.os_full = os_full
        self.package_name = package_name
        self.package_version = package_version
        self.package_type = package_type
        self.reference = reference
        self.remediation = remediation
        self.detected_at = detected_at or datetime.utcnow()

    @staticmethod
    def from_excel_row(row, remediation):
        is_flat = any('.' in key for key in row.keys())

        def get_value(flat_key, nested_keys):
            if is_flat:
                return row.get(flat_key)
            value = row
            for key in nested_keys:
                value = value.get(key, {}) if isinstance(value, dict) else {}
            return value or None

        detected_at = get_value('vulnerability.detected_at', ['vulnerability', 'detected_at'])
        if detected_at:
            detected_at = parse_detected_at(detected_at)

        return Vulnerability(
            cve_id=get_value('vulnerability.id', ['vulnerability', 'id']),
            severity=get_value('vulnerability.severity', ['vulnerability', 'severity']),
            description=get_value('vulnerability.description', ['vulnerability', 'description']),
            os_name=get_value('host.os.name', ['host', 'os', 'name']),
            os_platform=get_value('host.os.platform', ['host', 'os', 'platform']),
            os_full=get_value('host.os.full', ['host', 'os', 'full']),
            package_name=get_value('package.name', ['package', 'name']),
            package_version=get_value('package.version', ['package', 'version']),
            package_type=get_value('package.type', ['package', 'type']),
            reference=get_value('vulnerability.reference', ['vulnerability', 'reference']),
            remediation=remediation,
            detected_at=detected_at
        )

    def to_dict(self):
        return {
            "cve_id": self.cve_id,
            "severity": self.severity,
            "description": self.description,
            "host": {
                "os_name": self.os_name,
                "os_platform": self.os_platform,
                "os_full": self.os_full
            },
            "package": {
                "name": self.package_name,
                "version": self.package_version,
                "type": self.package_type
            },
            "reference": self.reference,
            "remediation": self.remediation,
            "detected_at": self.detected_at
        }

    def insert(self):
        return self.collection.insert_one(self.to_dict()).inserted_id

    @classmethod
    def get_one(cls, query):
        return cls.collection.find_one(query)

    @classmethod
    def get_all(cls, query={}):
        return list(cls.collection.find(query))
    
    @classmethod
    def count(cls, query={}):
        return cls.collection.estimated_document_count(query)


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
    
    
