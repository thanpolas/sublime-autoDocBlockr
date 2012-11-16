import sublime

import jsdocs
import modules.commentsParser
import modules.commentsUpdate
import modules.commentsWrite
import modules.sublimeHelper

def init(mem, view):
    """Reset and initialize important variables"""



    mem.cursorPoint = mem.view.sel()[0].end()
    mem.parser = jsdocs.getParser(mem.view)

    mem.parser.inline = False

    mem.subHelp = modules.sublimeHelper.SublimeHelper(mem)

    # Get basic orianation
    mem.cursorCol = mem.subHelp.getCol(mem.cursorPoint)
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
        initDocs(mem)
        #and exit
        return False

    return True

def initDocs(mem):
    (row,col) = mem.view.rowcol(mem.view.sel()[0].begin())

    # Move the cursor one line up
    target = mem.view.text_point(row - 1, 0)
    mem.view.sel().clear()
    mem.view.sel().add(sublime.Region(target))

    row = mem.subHelp.getRow(mem.cursorPoint)
    mem.subHelp.positionCursor(row)
    mem.subHelp.insertNewLine()
    #mem.subHelp.insertNewLine(True)
    mem.subHelp.writeString("/**")
    # Create the docblock
    mem.view.run_command("jsdocs")
