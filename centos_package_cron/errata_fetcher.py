# coding: utf8

from errata_item import *
import urllib2
import contextlib
from os.path import exists
from ConfigParser import RawConfigParser

from xml.etree import ElementTree as et
from package_parser import PackageParser

YUM_CONF = "/etc/yum.conf"
ERRATA_URL = "https://cefs.steve-meier.de/errata.latest.xml"


def get_opener():
    default_opener = urllib2.build_opener()
    if not exists(YUM_CONF):
        return default_opener
    config = RawConfigParser()
    config.read(YUM_CONF)
    if not config.has_section('main'):
        return default_opener
    if not config.has_option('main', 'proxy'):
        return default_opener
    proxy = {}
    url = config.get('main', 'proxy').strip()
    if not url:
        return default_opener
    http_proxy_handler = urllib2.ProxyHandler({'http': url, 'https': url})
    # urllib2 can open HTTPS ressources through a proxy since python 2.6.3
    # should be OK on Centos OS (Python 2.6.6)
    if config.has_option('main', 'proxy_username') and config.has_option(
            'main', 'proxy_password'):
        username = config.get('main', 'proxy_username').strip()
        password = config.get('main', 'proxy_password').strip()
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, url, username, password)
        proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_manager)
        return urllib2.build_opener(http_proxy_handler, proxy_auth_handler)
    return urllib2.build_opener(http_proxy_handler)


class ErrataParser:

    def getType(self, theType):
        mapping = {
            'Bug Fix Advisory': ErrataType.BugFixAdvisory,
            'Security Advisory': ErrataType.SecurityAdvisory,
            'Product Enhancement Advisory':
            ErrataType.ProductEnhancementAdvisory
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

    def parseSingleItem(self, node):
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
            packages = map(lambda x: PackageParser.parsePackage(x.text),
                           node.findall('packages'))
            references = node.attrib.get('references').split(' ')
            return ErrataItem(node.tag, the_type, severity, architectures,
                              releases, packages, references)
        except:
            print "Problem while parsing node %s" % (node)
            raise

    def parse(self, xml_str):
        dom = et.fromstring(xml_str)
        assert dom.tag == 'opt', "Expecting doc root to be opt but was %s" % (
            doc.localName)
        result = map(lambda x: self.parseSingleItem(x), dom)
        result = list(filter(lambda x: x != None, result))
        return result


class ErrataFetcher:

    def get_errata(self):
        with contextlib.closing(get_opener().open(ERRATA_URL)) as response:
            xml = response.read()
        parser = ErrataParser()
        return parser.parse(xml)

