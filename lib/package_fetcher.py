import os
import sys
import yum

class Package:
	def __init__(self,name,version,release,arch):
		self.name = name
		self.version = version
		self.release = release
		self.arch = arch
	def __str__(self):
		return "Package %s-%s-%s" % (self.name, self.version, self.release)
	def __repr__(self):
		return self.__str__()

class PackageFetcher:
	def __init__(self):
		self.yb = yum.YumBase()
		self.yb.setCacheDir()
	
	def fetch_installed_packages(self):		
		packages = self.yb.rpmdb.returnPackages()
		result = map(lambda x: Package(x.name,x.version,x.release, x.arch), packages)
		return result

	def get_package_updates(self):
		raw_updates = self.yb.update()
		result = map(lambda x: Package(x.name,x.version,x.release, x.arch), raw_updates)
		return result
		