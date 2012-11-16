import re

import sublime

class SublimeHelper():

    def __init__(self, mem):
        self.gc = mem
        self.sublime = self.gc
        self.view = self.gc.view
        self.edit = self.gc.edit

    def positionCursor(self, row, col=0):
        target = self.view.text_point(row, col)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))
        return target

    def positionCursrorPoint(self, point):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(point))

    def selectLine(self, row, col=0):
        target = self.positionCursor(row, col)
        lineSelection = self.view.full_line(sublime.Region(target))
        self.view.sel().add(lineSelection)
        return lineSelection

    def removeLine(self, row):
        lineSelection = self.selectLine(row)
        self.view.erase(self.edit, lineSelection)

    def insertSnippet(self, snippet):
        """Insert the snippet at current cursor position"""
        self.view.run_command(
            'insert_snippet', {
                'contents': snippet
            }
        )

    def insertNewLine(self, leaveCursror=False):
        """Insert a new line at current position and return back"""
        currentPos = self.getCurrentSelStartPoint()
        self.writeString('\n', currentPos)
        if not leaveCursror:
            self.positionCursrorPoint(currentPos)

    def writeString(self, string, point=None):
        if not point:
            point=self.getCurrentSelEndPoint()
        self.view.insert(self.edit, point, string)

    def getRowCol(self, currentPoint=None):
        if currentPoint:
            usePoint = currentPoint
        else:
            usePoint = self.getCurrentSelEndPoint()

        return self.view.rowcol(usePoint)

    def getRow(self, cursorPoint=None):
        return self.getRowCol(cursorPoint)[0]

    def getCol(self, cursorPoint=None):
        return self.getRowCol(cursorPoint)[1]

    def getCurrentSelStartPoint(self):
        return self.view.sel()[0].begin()

    def getCurrentSelEndPoint(self):
        return self.view.sel()[0].end()

    def getLastLine(parser, view, currentPoint):
        return parser.getDefinition(view, view.line(currentPoint).begin() - 1)

    def read_line(self, point=None):
        if not point:
            point = self.getCurrentSelEndPoint()

        if (point >= self.view.size()):
            return
        next_line = self.view.line(point)
        return self.view.substr(next_line)


    def getIndendation(self, strLine=None):
        """return a string with indentation"""

        reSpaces = re.compile(r"\s*")
        if not strLine:
            # Get the current line
            return reSpaces.match(self.read_line()).group(0)

        return reSpaces.match(strLine).group(0)

