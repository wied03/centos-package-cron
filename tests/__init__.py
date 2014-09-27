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
		'tests.test_errata_fetcher',
		'tests.test_mockable_execute',
		'tests.test_os_version_fetcher.py',
		'tests.test_package_checker.py',
		'tests.test_package_fetcher.py'
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
