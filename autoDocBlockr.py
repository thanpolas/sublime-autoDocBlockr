"""
autoDocBlockr v0.1.0
by Thanasis Polychronakis
https://github.com/thanpolas/sublime-autoDocBlockr
"""

import sublime
import sublime_plugin

# plat_lib_path = os.path.join(sublime.packages_path(), 'modules')
# m_info = imp.find_module('commentsParser', [plat_lib_path])
# m = imp.load_module('modules', *m_info)


#from modules.commentsParser import *
# import modules
import modules.commentsParser
import modules.commentsUpdate
import modules.commentsWrite
import modules.sublimeHelper

#import globalClass

# Check if jsdocs exists and load it
try:
    import jsdocs
    hasJsDocs = True
except:
    hasJsDocs = False






class Mem:
    def reset(self):
        # The sublime view object
        self.view=None
        # The sublime edit object
        self.edit=None
        # The current cursorPoint
        self.cursorPoint=None
        # The cursor's column when everything started...
        self.cursorCol=None
        # The function's row as is tranformed by how / what we edit
        self.currentFnRow=None
        # The jsdoc parser class
        self.parser=None
        # The contents of the current line (string)
        self.currentLine=None
        # An array with the document block elements
        self.docBlockOut=None
        # a tuple with the funciton name, all arguments, and at the end
        # a guessed return value
        self.funcArgs=None
        # The raw function argument string
        self.args=None
        # A list of tuples with the function arguments
        # Each tuple has a guess at the type and the name of the argument.
        self.parsedArgs=None
        # A list of the function arguments
        self.listArgs=None
        # The indentation of the current line as a string
        self.indent=None
        # current doc block matches in a list of dicts.
        self.matches=None
        # A dict describing the current docBlock coordinates
        self.docBlockCoords=None

mem = Mem()

class AutoDocBlockr(sublime_plugin.TextCommand):
    # will contain the comments_parser instance
    comParser = None

    def run(self, edit, trigger):
        global wrt
        if not hasJsDocs:
            errMsg = "DocBlockr package is required. "
            errMsg += "Get it from: https://github.com/spadgos/sublime-jsdocs"
            print errMsg
            return

        if not self.initialize(edit, self.view):
            self.defaultAction(trigger)
            return
        newDocBlock = mem.comUpdate.updateComments()
        mem.comWrite.writeComments(newDocBlock)

        self.defaultAction(trigger)

    def defaultAction(self, trigger):
        # position the cursor back to original position
        mem.subHelp.positionCursor(mem.currentFnRow, mem.cursorCol)

        if 'enter' == trigger:
            mem.subHelp.insertNewLine(True)
        elif 'down' == trigger:
            mem.subHelp.positionCursor(mem.currentFnRow + 1, mem.cursorCol)

    def initDocs(self):
        (row,col) = self.view.rowcol(self.view.sel()[0].begin())

        # Move the cursor one line up
        target = self.view.text_point(row - 1, 0)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))

        row = mem.subHelp.getRow(mem.cursorPoint)
        mem.subHelp.positionCursor(row)
        mem.subHelp.insertNewLine()
        #self.subHelp.insertNewLine(True)
        mem.subHelp.writeString("/**")
        # Create the docblock
        self.view.run_command("jsdocs")



    def initialize(self, edit, view):
        """Reset and initialize important variables"""

        mem.reset()

        mem.view= view
        mem.edit= edit

        mem.cursorPoint = mem.view.sel()[0].end()
        mem.parser = jsdocs.getParser(mem.view)

        mem.parser.inline = False

        mem.subHelp = modules.sublimeHelper.SublimeHelper(mem)
        # Get basic orianation
        mem.cursorCol = mem.subHelp.getCol()
        mem.currentFnRow = mem.subHelp.getRow()

        mem.settings = view.settings()
        if not mem.settings.get('autoDocBlockr'):
            return False

        # read the same line
        mem.currentLine = mem.parser.getDefinition(mem.view, mem.cursorPoint)
        # Check we are on a function declaration line
        if mem.currentLine:
            mem.docBlockOut = mem.parser.parse(mem.currentLine)
        else:
            return False

        if not mem.docBlockOut:
            return False

        # Get the function arguments and parse them
        mem.funcArgs = mem.parser.parseFunction(mem.currentLine)
        if not mem.funcArgs:
            return False

        mem.args = mem.funcArgs[1]

        # tuple: [(None, u'param1'), (None, u'param2')]
        # Fix for a bug that i need to address in jsdocs.py line
        # ~354, return an empty array if no args exist
        if mem.args:
            mem.parsedArgs = mem.parser.parseArgs(mem.args)
        else:
            mem.parsedArgs = []

        mem.listArgs = []
        for i, v in enumerate(mem.parsedArgs):
            mem.listArgs.append(v[1])

        # Initialize the classes we'll use
        reload(modules.commentsParser)
        reload(modules.commentsUpdate)
        reload(modules.commentsWrite)
        reload(modules.sublimeHelper)

        mem.comParser = modules.commentsParser.CommentsParser(mem)
        mem.comUpdate = modules.commentsUpdate.CommentsUpdate(mem)
        mem.comWrite = modules.commentsWrite.CommentsWrite(mem)

        # Get the indentation of the current line
        mem.indent = mem.subHelp.getIndendation()

        # get current docBlock matches
        mem.matches = mem.comParser.parseComments(mem)

        if None == mem.matches:
            # no comments found, create
            self.initDocs()
            #and exit
            return False

        return True



