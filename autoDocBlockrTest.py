# Based on the VintageEx tests
# https://github.com/SublimeText/VintageEx
#

import sublime
import sublime_plugin

import os
import sys
import unittest
import StringIO

import modules

#sys.path.append(os.path.join(sublime.packages_path(), 'autoDocBlockr/test'))

#from tests.jsParser_test import TestJsFunctionType
#from test import jsParser_test

#import test.jsparser_test

#reload(test)
#reload(unittest)

# TEST_DATA_FILE_BASENAME = 'vintageex_test_data.txt'
# TEST_DATA_PATH = os.path.join(sublime.packages_path(),
#                               'VintageEx/tests/data/%s' % TEST_DATA_FILE_BASENAME)


from autoDocBlockr import modules
import modules.jsParser_test

reload(modules.jsParser_test)

g_test_view = None
g_executing_test_suite = None

test_suites = {
        'jsParser': ['wtfbbq', 'autoDocBlockr.modules.jsParser_test']
}


def print_to_view(view, obtain_content):
    edit = view.begin_edit()
    view.insert(edit, 0, obtain_content())
    view.end_edit(edit)
    view.set_scratch(True)

    return view

#
class autoDocBlockrTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.run_suite(0)

    def run_suite(self, idx):
        global g_executing_test_suite

        suite_name = sorted(test_suites.keys())[idx]
        g_executing_test_suite = suite_name
        command_to_run, _ = test_suites[suite_name]

        bucket = StringIO.StringIO()
        _, suite = test_suites[suite_name]
        suite = unittest.defaultTestLoader.loadTestsFromName(suite)
        unittest.TextTestRunner(stream=bucket, verbosity=1).run(suite)

        print_to_view(self.window.new_file(), bucket.getvalue)



class autoRunTestCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return os.getcwd() == os.path.join(sublime.packages_path(), 'test')

    def run(self, suite_name):
        print "Got"
        bucket = StringIO.StringIO()
        _, suite = test_suites[suite_name]
        print _
        return
        suite = unittest.defaultTestLoader.loadTestsFromName(suite)
        unittest.TextTestRunner(stream=bucket, verbosity=1).run(suite)

        print_to_view(self.window.new_file(), bucket.getvalue)


