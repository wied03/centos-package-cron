version := $(shell ./setup.py -V)

centos-package-cron.spec:
	cp centos-package-cron.spec.in centos-package-cron.spec
	sed -i /s/THE_VERSION/$(version)/g centos-package-cron.spec
