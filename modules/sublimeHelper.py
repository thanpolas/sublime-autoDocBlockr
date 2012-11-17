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

    def removeLine(self, row, how_many=1):
        lastLinePoint = startPoint= self.view.text_point(row, 0)
        if 1 < how_many:
            lastLinePoint = self.view.text_point(row + how_many - 1, 0)
        endPoint = self.view.full_line(lastLinePoint).end()
        lineRegion = sublime.Region(startPoint, endPoint)
        self.view.erase(self.edit, lineRegion)

    def insertSnippet(self, snippet):
        """Insert the snippet at current cursor position"""
        self.view.run_command(
            'insert_snippet', {
                'contents': snippet
            }
        )
    def insert(self, point, string):
        self.view.insert(self.edit, point, string)

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

    def _getPoint(self, currentPoint=None):
        return currentPoint if not None else self.getCurrentSelEndPoint()

    def getRow(self, cursorPoint=None):
        return self.getRowCol(cursorPoint)[0]

    def getCol(self, cursorPoint=None):
        return self.getRowCol(cursorPoint)[1]

    def getRowLastPoint(self, cursorPoint=None, cursorIsRow=False):
        if cursorIsRow: cursorPoint=self.view.text_point(cursorPoint, 0)
        return self.view.line(self._getPoint(cursorPoint)).end()
    def getRowFirstPoint(self, cursorPoint=None, cursorIsRow=False):
        if cursorIsRow: cursorPoint=self.view.text_point(cursorPoint, 0)
        return self.view.line(self._getPoint(cursorPoint)).begin()

    def getCurrentSelStartPoint(self):
        # When no selection
        # self.view.sel() == [(18369, 18369)]
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

