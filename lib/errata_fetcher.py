class ErrataType:
	BugFixAdvisory = range(1)

class ErrataItem:
	def __init__(self,advisory_id,type,severity,architectures,releases,packages):
		self.advisory_id = advisory_id
		self.type = type
		self.severity = severity
		self.architectures = architectures
		self.releases = releases
		self.packages = packages

class ErrataParser:
	def parse(self,xml):
		raise 'implement this'

class ErrataFetcher:
	def get_errata(self):
		raise 'implement this'
	