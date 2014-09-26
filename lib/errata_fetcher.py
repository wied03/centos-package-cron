#import xml.dom.minidom
from xml.etree import ElementTree as et

class ErrataType:
	BugFixAdvisory = range(1)
	
class ErrataSeverity:
	Important = range(1)

class ErrataItem:
	def __init__(self,advisory_id,type,severity,architectures,releases,packages):
		self.advisory_id = advisory_id
		self.type = type
		self.severity = severity
		self.architectures = architectures
		self.releases = releases
		self.packages = packages

class ErrataParser:
	def getType(self,theType):
		mapping = {
		'Bug Fix Advisory': ErrataType.BugFixAdvisory
		}
		try:
			return mapping[theType]
		except KeyError:
			print "Do not understand mapping for type %s" % (theType)
			raise
			
	def getSeverity(self, theSeverity):
		if theSeverity == None:
			return None
		mapping = {
		'Important': ErrataSeverity.Important
		}
		try:
			return mapping[theSeverity]
		except KeyError:
			print "Do not understand mapping for severity %s" % (theSeverity)
			raise
	
	def parseSingleItem(self,node):		
		the_type = self.getType(node.attrib['type'])
		severity = self.getSeverity(node.attrib.get('severity'))
		architectures = map(lambda x: x.text, node.findall('os_arch'))
		releases = map(lambda x: x.text, node.findall('os_release'))
		packages = map(lambda x: x.text, node.findall('packages'))
		return ErrataItem(node.tag, the_type, severity, architectures, releases, packages)
	
	def parse(self,xml_str):
		dom = et.fromstring(xml_str)
		assert dom.tag == 'opt', "Expecting doc root to be opt but was %s" % (doc.localName)
		return map(lambda x: self.parseSingleItem(x), dom)		

class ErrataFetcher:
	def get_errata(self):
		raise 'implement this'
	