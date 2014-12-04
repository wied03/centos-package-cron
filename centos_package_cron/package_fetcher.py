import os
import sys
import yum
import re
import mockable_execute
from package import Package
from package_parser import PackageParser
        
class ChangeLogParser:
    def get_log_version_num_with_release_suffix(self,version,release):
        match = re.match(r'^.*?(\S+)\.el\S+\.(\d+)$', release)
        return version + '-' + match.group(1) + '.' + match.group(2) if match else None
    
    def get_log_version_num_without_release_suffix(self,version,release):
        match = re.match(r'^.*?(\S+)\.el\S+$', release)
        return version + '-' + match.group(1)  if match else None
    
    def get_log_version_nums(self,version,release): 
        versions = [self.get_log_version_num_with_release_suffix(version,release),
        self.get_log_version_num_without_release_suffix(version,release),
        version + '-' + release]
        return list(filter(lambda v: v != None,versions))
                    
    def get_regex_patterns(self,name,version,release):
        versions = self.get_log_version_nums(version,release)
        escaped_package_name = re.escape(name)
        pattern_former = lambda v: r'.*^(?:\d+\:){0,1}' + escaped_package_name +r'.*?(^\*.*? ' + re.escape(v) + r'.*?)^\*.*'        
        patterns = map(pattern_former,versions)
        return patterns
    
    def get_regexes(self,name,version,release):
        return map(lambda pat: re.compile(pat,re.MULTILINE | re.DOTALL), self.get_regex_patterns(name,version,release))     
    
    def parse(self,output,name,version,release):
        regexes = self.get_regexes(name,version,release)
        matches = map(lambda r: r.match(output), regexes)
        match = next((match for match in matches if match != None), None)   
        if match == None:
            return "Unable to parse changelog for package %s version %s release %s" % (name,version,release)
        return match.group(1)

class PackageFetcher:
    def __init__(self,changelog_parser,executor,repos_to_exclude=[],repos_to_include=[]):
        self.changelog_parser = changelog_parser
        self.yb = yum.YumBase()
        self.yb.setCacheDir()
        self.executor = executor
        self.repos_to_exclude = repos_to_exclude
        self.repos_to_include = repos_to_include
        for repo in repos_to_exclude:
            self.yb.repos.disableRepo(repo)
        for repo in repos_to_include:
            self.yb.repos.enableRepo(repo)
    
    def fetch_installed_packages(self):     
        packages = self.yb.rpmdb.returnPackages()
        result = map(lambda x: Package(x.name,x.version,x.release, x.arch, x.repoid), packages)
        return result

    def get_package_updates(self):
        raw_updates = self.yb.update()
        result = map(lambda x: Package(x.name,x.version,x.release, x.arch, x.repoid), raw_updates)
        return result
        
    def get_what_depends_on(self,name):
        command = ['rpm', '-q', '--provides', name]
        output = self.executor.run_command(command)        
        command = ['sed', r'''s/^/"/;s/\([^[:space:]]\) *$/\1"/;/=/{h;s/ =.*$/"/;G}''']
        output = self.executor.run_command(command, command_input=output)
        command = ['xargs', 'rpm', '-q', '--whatrequires']
        output = self.executor.run_command(command, command_input=output)
        command = ['grep', '-v', '-E', r'''^no package''']
        packages = self.executor.run_command(command, command_input=output)
        packages = packages.split("\n")
        packages = sorted(packages)
        packages = list(set(packages))
        packages = list(filter(lambda v: v != "",packages))
        packages = map(lambda pkgStr: PackageParser.parsePackage(pkgStr), packages)
        return map(lambda pkgHsh: Package(pkgHsh['name'], pkgHsh['version'], pkgHsh['release'], pkgHsh['arch'], repository=""), packages)
        
    def get_package_changelog(self,name,version,release):
        args = ['/usr/bin/yum']
        if len(self.repos_to_exclude) > 0:
            repos_flat = "--disablerepo=%s" % (','.join(self.repos_to_exclude))
            args.append(repos_flat)
        if len(self.repos_to_include) > 0:
            repos_flat = "--enablerepo=%s" % (','.join(self.repos_to_include))
            args.append(repos_flat)
        args += ['changelog', 'updates', name]                  
        output = self.executor.run_command(args)
        return self.changelog_parser.parse(output,name,version,release)
        