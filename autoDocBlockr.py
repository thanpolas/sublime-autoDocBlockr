"""
autoDocBlockr v0.1.3
by Thanasis Polychronakis
https://github.com/thanpolas/sublime-autoDocBlockr
"""

__author__ = 'thanpolas@gmail.com (Thanasis Polychronakis)'

import sys
import logging

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
reload(modules.jsdocs)




logger = logging.getLogger('autoDocBlockr')
# Set to WARNING or DEBUG
logger.setLevel(logging.DEBUG)

if (0 == len(logger.handlers)):
    formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s.%(funcName)s():%(lineno)d:: %(message)s')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

logger.info("Loading...")


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
        self.parsedFuncArgs=None
        # A list of the function arguments
        self.listArgs=None
        # The indentation of the current line as a string
        self.indent=None
        # current doc block matches in a list of dicts.
        self.matches=None
        # A dict describing the current docBlock coordinates
        self.docBlockCoords=None


#mem = Mem()


# Check if jsdocs exists and load it
try:
    import modules.jsdocs as jsdocs
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

    triggered=False

    def __init__(self):
        super(BackgroundAutoDoc, self).__init__()

    def on_query_context(self, view, key, operator, operand, match_all):
        if key in view.settings().get('autoDocBlocr_trigger_on'):
            # A lame workaround for throttling events
            # up and down events gets triggered twice
            #print key + "::" + str(self.triggered)
            if not self.triggered:
                self.triggered=True
                sublime.set_timeout(self.close_trigger, 150)
                start_autoDocBlockr(view, "event")
            return False

    def close_trigger(self):
        self.triggered=False

######################

class AutoDocBlockr(sublime_plugin.TextCommand):

    def run(self, edit, trigger):
        start_autoDocBlockr(self.view, trigger)

class AutoDocBlockrVoid(sublime_plugin.TextCommand):
    def run(self, edit):
        # do nothing
        return False

#####################


def start_autoDocBlockr(view, trigger):
    """Start autoDocBlockr"""
    mem = Mem()
    mem.view=view
    mem.settings = view.settings()
    if not mem.settings.get('autoDocBlockr'):
        return False

    # try:
    #     reload(modules.initialize)
    # except RuntimeError, ex:
    #     print "autoDocBlockr Exception on modules.initialize reload"
    #     print ex
    #     return

    if not modules.eventHandler.checkSyntax(view):
        return

    mem.edit=view.begin_edit('autoDocBlockr')

    if not modules.initialize.init(mem, view):
        mem.view.end_edit(mem.edit)
        return

    newDocBlock = mem.comUpdate.updateComments()

    mem.comWrite.writeComments(newDocBlock)

    mem.view.end_edit(mem.edit)







