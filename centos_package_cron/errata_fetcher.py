from errata_item import *
import urllib2
from xml.etree import ElementTree as et
from package_parser import PackageParser

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
            # Sometimes empty elements are in there
            if 'type' not in node.attrib:
                return None
            the_type = self.getType(node.attrib['type'])
            severity = self.getSeverity(node.attrib.get('severity'))
            architectures = map(lambda x: x.text, node.findall('os_arch'))
            releases = map(lambda x: x.text, node.findall('os_release'))
            packages = map(lambda x: PackageParser.parsePackage(x.text), node.findall('packages'))
            references = node.attrib.get('references').split(' ')
            return ErrataItem(node.tag, the_type, severity, architectures, releases, packages, references)
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
        response = urllib2.urlopen('https://cefs.steve-meier.de/errata.latest.xml')
        xml = response.read()
        parser = ErrataParser()
        return parser.parse(xml)

