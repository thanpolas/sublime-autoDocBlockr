"""
autoDocBlockr v0.1.0
by Thanasis Polychronakis
https://github.com/thanpolas/sublime-autoDocBlockr
"""
import sys

import sublime
import sublime_plugin

# import modules
import modules.eventHandler
import modules.initialize
import modules.commentsParser
import modules.commentsUpdate
import modules.commentsWrite
import modules.sublimeHelper

reload(modules.eventHandler)
reload(modules.initialize)
reload(modules.commentsParser)
reload(modules.commentsUpdate)
reload(modules.commentsWrite)
reload(modules.sublimeHelper)

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


# Check if jsdocs exists and load it
try:
    import jsdocs
except:
    errMsg = "To run autoDocBlockr the DocBlockr package is required. "
    errMsg += "Get it from: https://github.com/spadgos/sublime-jsdocs"
    sublime.error_message(errMsg)
    #sys.exit()

def last_selected_lineno(view):
    viewSel = view.sel()
    if not viewSel:
        return None
    return view.rowcol(viewSel[0].end())[0]

class BackgroundAutoDoc(sublime_plugin.EventListener):
    '''TBD
    '''

    def __init__(self):
        super(BackgroundAutoDoc, self).__init__()
        self.lastSelectedLineNo = -1

    def on_selection_modified(self, view):
        if view.is_scratch():
            return

        if not view.settings().get('autoDocBlockr'):
            return False

        lastSelectedLineNo = last_selected_lineno(view)

        if not modules.eventHandler.checkSyntax(view):
            return

        if lastSelectedLineNo != self.lastSelectedLineNo:
            self.lastSelectedLineNo = lastSelectedLineNo
            #start_autoDocBlock(view, 'event')




######################

class AutoDocBlockr(sublime_plugin.TextCommand):

    def run(self, edit, trigger):
        start_autoDocBlock(self.view, trigger)

#####################


def start_autoDocBlock(view, trigger):
    reload(modules.initialize)
    if not modules.eventHandler.checkSyntax(view):
        return

    mem.reset()
    mem.view= view
    mem.edit= view.begin_edit('autoDocBlockr')
    if not modules.initialize.init(mem, view):
        defaultAction(trigger)
        mem.view.end_edit(mem.edit)
        return


    newDocBlock = mem.comUpdate.updateComments()
    mem.comWrite.writeComments(newDocBlock)

    defaultAction(trigger)
    mem.view.end_edit(mem.edit)

def defaultAction(trigger):
    # position the cursor back to original position
    mem.subHelp.positionCursor(mem.currentFnRow, mem.cursorCol)

    if 'enter' == trigger:
        mem.subHelp.insertNewLine(True)
    elif 'down' == trigger:
        mem.subHelp.positionCursor(mem.currentFnRow + 1, mem.cursorCol)





