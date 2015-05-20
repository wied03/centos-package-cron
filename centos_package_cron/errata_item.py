from datetime import datetime
from db_base import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey

class ErrataType:
    BugFixAdvisory,SecurityAdvisory,ProductEnhancementAdvisory = range(3)
    
    @staticmethod
    def get_label(value):
        labels = {
        ErrataType.BugFixAdvisory: 'Bug Fix Advisory',
        ErrataType.SecurityAdvisory: 'Security Advisory',
        ErrataType.ProductEnhancementAdvisory: 'Product Enhancement Advisory'
        }
        return labels[value]
    
class ErrataSeverity:
    Critical, Important, Moderate, Low = range(4)
    
    @staticmethod
    def get_label(value):
        labels = {
        ErrataSeverity.Important: 'Important',
        ErrataSeverity.Moderate: 'Moderate',
        ErrataSeverity.Low: 'Low',
        ErrataSeverity.Critical: 'Critical',
        None: '(No severity supplied)'
        }
        return labels[value]

class ErrataItem(Base):
    __tablename__ = 'notified_advisories'
    id = Column(Integer, primary_key=True)
    advisory_id = Column(String)
    timestamp = Column(DateTime)
    
    def __init__(self,advisory_id,type,severity,architectures,releases,packages,references):
        self.advisory_id = advisory_id
        self.type = type
        self.severity = severity
        self.architectures = architectures
        self.releases = releases
        self.packages = packages
        self.references = references
        self.timestamp = datetime.today()
