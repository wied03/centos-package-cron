complete_version := $(shell ./setup.py -V)
spaced_version := $(subst ., ,$(complete_version))
dist := $(lastword $(spaced_version))
version := $(subst .$(dist),,$(complete_version))

clean:
	rm -f centos-package-cron.spec

centos-package-cron.spec:
	cp centos-package-cron.spec.in centos-package-cron.spec
	sed -i.bak 's/THE_VERSION/$(version)/g' centos-package-cron.spec
	sed -i.bak 's/THE_DIST/$(dist)/g' centos-package-cron.spec
	rm centos-package-cron.spec.bak
