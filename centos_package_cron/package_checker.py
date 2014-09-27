class PackageChecker:
	def __init__(self, errata_fetcher, package_fetcher, os_fetcher):
		self.errata_fetcher = errata_fetcher
		self.package_fetcher = package_fetcher
		self.os_fetcher = os_fetcher
	
	def match_advisory_against_installed(self,advisory_package,current_installed):
		return any(advisory_package['name'] == inst.name and  
		(advisory_package['version'] > inst.version or
		(advisory_package['version'] == inst.version and advisory_package['release'] > inst.release)) for inst in current_installed)
	
	def findAdvisoriesOnInstalledPackages(self):
		os_version = self.os_fetcher.get_top_level_version()
		advisories = self.errata_fetcher.get_errata()
		current_installed = self.package_fetcher.fetch_installed_packages()
		pkg_match = lambda adv_pkgs: any(self.match_advisory_against_installed(adv_pkg,current_installed) for adv_pkg in adv_pkgs)
		top_level_match = lambda adv: os_version in adv.releases and pkg_match(adv.packages)
		return list(filter(top_level_match,advisories))	
	