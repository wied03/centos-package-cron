class PackageChecker:
	def __init__(self, errata_fetcher, package_fetcher, os_fetcher):
		self.errata_fetcher = errata_fetcher
		self.package_fetcher = package_fetcher
		self.os_fetcher = os_fetcher
	
	def findAdvisoriesOnInstalledPackages(self):
		os_version = self.os_fetcher.get_top_level_version()
		advisories = self.errata_fetcher.get_errata()
		current_installed = self.package_fetcher.fetch_installed_packages()
		only_our_packages = lambda adv: os_version in adv.releases
		return list(filter(only_our_packages,advisories))		
	