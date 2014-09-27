import unittest

def additional_tests(suite=None):
    import centos_package_cron
    if suite is None:
        suite = unittest.TestSuite()
    return suite


def all_tests_suite():
    def get_suite():
        return additional_tests(
            unittest.TestLoader().loadTestsFromNames([
		'tests.errata_fetcher',
		'tests.mockable_execute',
		'tests.os_version_fetcher.py',
		'tests.package_checker.py',
		'tests.package_fetcher.py'
            ]))
    suite = get_suite()
    import centos_package_cron 
    return suite


def main():
    runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
    suite = all_tests_suite()
    raise SystemExit(not runner.run(suite).wasSuccessful())


if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()
