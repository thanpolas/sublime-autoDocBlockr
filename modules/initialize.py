import re
import logging

import modules.jsdocs as jsdocs
import modules.commentsParser
import modules.commentsUpdate
import modules.commentsWrite
import modules.sublimeHelper
import modules.eventHandler
import modules.jsParser

module_logger = logging.getLogger('autoDocBlockr.initialize')

def init(mem, view):
    """Reset and initialize important variables"""

    mem.cursorPoint = mem.view.sel()[0].end()
    mem.lineStartPoint = view.line(mem.cursorPoint).begin()
    mem.parser = jsdocs.getParser(mem.view)

    mem.parser.inline = False

    mem.subHelp = modules.sublimeHelper.SublimeHelper(mem)

    # Get basic orianation
    mem.cursorCol = mem.subHelp.getCol(mem.cursorPoint)
    mem.currentFnRow = mem.subHelp.getRow()

    # read the same line. Use line start point or jsdocs parser gets crazy
    mem.currentLine = mem.parser.getDefinition(mem.view, mem.lineStartPoint)

    # Check we are on a function declaration line
    if not mem.currentLine:
        return False

    mem.docBlockOut = mem.parser.parse(mem.currentLine)

    if "javascript" == modules.eventHandler.syntax_name(mem.view).lower():
        # Check if function is proper to add docBlockr
        if not modules.jsParser.properFunc(mem.currentLine):
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
        mem.parsedFuncArgs = mem.parser.parseArgs(mem.args)
    else:
        mem.parsedFuncArgs = []

    mem.listArgs = []
    for i, v in enumerate(mem.parsedFuncArgs):
        mem.listArgs.append(v[1])

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

    module_logger.info('Passed initialization. row:' + str(mem.currentFnRow) + ' col:' + str(mem.cursorCol))
    return True

def initDocs(mem):
    # Add a new line at the current line where the func declaration was
    mem.subHelp.positionCursor(mem.currentFnRow)
    mem.subHelp.insertNewLine()
    # Echo the string that triggers DocBlockr
    mem.subHelp.writeString(mem.indent + "/**")
    # Create the docblock
    mem.view.run_command("jsdocs")

    # Locate row where the func now is
    find_result = mem.view.find(re.escape(mem.currentLine),
        mem.subHelp.getCurrentSelStartPoint())
    if find_result is None:
        module_logger.error('Could not find function line to position cursor. fn line searched:' + mem.currentLine)
        return

    row = mem.subHelp.getRow(find_result.begin())

    #module_logger.info('Func found at row:' + str(row))
    # Return the cursor back where it was
    mem.subHelp.positionCursor(row, mem.cursorCol)


