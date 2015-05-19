import re

class OsVersionFetcher:
    def get_complete_version(self):
        version_file = open('/etc/centos-release')
        try:
            version_string = version_file.read()
            return re.match(r'.*?(\d+\S+)\s.*',version_string).group(1)
        finally:
            version_file.close
        
    def get_top_level_version(self):
        complete = self.get_complete_version()
        return re.match(r'.*?(\d+)\..*',complete).group(1)
        
    def get_mid_level_version(self):
        complete = self.get_complete_version()
        return re.match(r'(\d+\.\d+).*', complete).group(1)
