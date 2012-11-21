
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
# cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
# if cmd_folder not in sys.path:
#     sys.path.insert(0, cmd_folder)

# # # use this if you want to include modules from a subforder
# cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"..")))
# if cmd_subfolder not in sys.path:
#     sys.path.insert(0, cmd_subfolder)


# cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"..")))
# if cmd_subfolder not in sys.path:
#     sys.path.insert(0, cmd_subfolder)

import unittest

import jsParser


class TestJSParser(unittest.TestCase):

    def setUp(self):
        return

    def test_anon_funcs(self):
        funcStrings = {
            'inline callback': "this.el.$modalWelcomeBtn.on('click', goog.bind(Function(){}, this));",
            'define optional callback': 'var fn = opt_fn || function(){};'
            }

        for descr, test_string in funcStrings.iteritems():
            self.assertFalse(jsParser.properFunc(test_string), descr)


    def test_iffy_funcs(self):
        funcStrings = {
            'full':  "(function(){})()",
            'bang':  "!function(){",
            'bang space':  "!function() {",
            'bang space with params':  "!function(opt_zoid, lor) {",
            'dash': "-function(){",
            'plus': "+function(){",
            'tilde': "~function(){"
        }

        for descr, test_string in funcStrings.iteritems():
            self.assertFalse(jsParser.properFunc(test_string), descr)



    def test_declaration_funcs(self):
        funcStrings = {
            'start of line': "function ball(){"
            }

        for descr, test_string in funcStrings.iteritems():
            self.assertTrue(jsParser.properFunc(test_string), descr)


        self.assertFalse(jsParser.properFunc('zit.forEach(function zitForEach(item){'), 'an inline func declaration')

    def test_expression_funcs(self):
        funcStrings = {
            'typical': "ball.app = function()",
            'another expression': "   an.expression.func = function(){}",
            'inside an object with string literal': "  'keyInAnObject' : function() {}",
            'inside an object': "   keyInAnObject : function(){}            "
            }

        for descr, test_string in funcStrings.iteritems():
            self.assertTrue(jsParser.properFunc(test_string), descr)




    def test_new_funcs(self):
        funcStrings = {
            'odd case at beginning of line': "New function()",
            'typical': "var zol= New Function()"
            }

        for descr, test_string in funcStrings.iteritems():
            self.assertFalse(jsParser.properFunc(test_string), descr)


if __name__ == '__main__':
    unittest.main()
