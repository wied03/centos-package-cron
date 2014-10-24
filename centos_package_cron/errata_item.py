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
        ErrataSeverity.Critical: 'Critical'
        }
        return labels[value]

class ErrataItem:
    def __init__(self,advisory_id,type,severity,architectures,releases,packages,references):
        self.advisory_id = advisory_id
        self.type = type
        self.severity = severity
        self.architectures = architectures
        self.releases = releases
        self.packages = packages
        self.references = references
