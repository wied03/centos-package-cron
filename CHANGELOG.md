# 1.0.9
* Simpler version scheme
* Pypi package documented (as of 1.0.8.1)
* Add HTTP proxy support (#16)
# Fixed issue (#18)

# 1.0.8.1
* Fix issue with encoding (#9)
* Fix issue with --skipold argument (#8). It's now inverted and named --forceold. Supplying the argument will ignore previously sent notices and send you everything.
* Email MTA has been removed from the RPM dependencies to allow easier stdout/Docker usage

# 1.0.7
* Improve rpmspec (test on CentOS 6.6, 6.7, and 7 with Travis)
* Update version string in application

# 1.0.6
* Use HTTPS when retrieving errata

# 1.0.5
* CentOS 6 compatibility fixes
* Errata severity fix
* Ability to send report to stdout
* Email, when used as output type, goes to root by default

# 1.0.4
* Adds "what depends on each package" to the updates

# 1.0.3
* Added database functionality to keep track of which updates you've already been notified about
