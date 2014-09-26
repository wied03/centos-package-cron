import urllib2
from xml.etree import ElementTree as et

class ErrataType:
	BugFixAdvisory,SecurityAdvisory,ProductEnhancementAdvisory = range(3)
	
class ErrataSeverity:
	Important, Moderate, Low, Critical = range(4)

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
		mapping = {'Bug Fix Advisory': ErrataType.BugFixAdvisory, 
		'Security Advisory':ErrataType.SecurityAdvisory, 
		'Product Enhancement Advisory':ErrataType.ProductEnhancementAdvisory}
		try:
			return mapping[theType]
		except KeyError:
			print "Do not understand mapping for type %s" % (theType)
			raise
			
	def getSeverity(self, theSeverity):
		if theSeverity == None:
			return None
		mapping = {
		'Important': ErrataSeverity.Important,
		'Moderate': ErrataSeverity.Moderate,
		'Low': ErrataSeverity.Low,
		'Critical': ErrataSeverity.Critical
		}
		try:
			return mapping[theSeverity]
		except KeyError:
			print "Do not understand mapping for severity %s" % (theSeverity)
			raise
	
	def parseSingleItem(self,node):
		try:
			if node.tag == 'meta':
				return None
			the_type = self.getType(node.attrib['type'])
			severity = self.getSeverity(node.attrib.get('severity'))
			architectures = map(lambda x: x.text, node.findall('os_arch'))
			releases = map(lambda x: x.text, node.findall('os_release'))
			packages = map(lambda x: x.text, node.findall('packages'))
			return ErrataItem(node.tag, the_type, severity, architectures, releases, packages)
		except:
			print "Problem while parsing node %s" % (node)
			raise
	
	def parse(self,xml_str):
		dom = et.fromstring(xml_str)
		assert dom.tag == 'opt', "Expecting doc root to be opt but was %s" % (doc.localName)
		result = map(lambda x: self.parseSingleItem(x), dom)
		result = list(filter(lambda x: x != None, result))
		return result

class ErrataFetcher:
	def get_errata(self):
		response = urllib2.urlopen('http://cefs.steve-meier.de/errata.latest.xml')
		xml = response.read()
		parser = ErrataParser()
		return parser.parse(xml)
	