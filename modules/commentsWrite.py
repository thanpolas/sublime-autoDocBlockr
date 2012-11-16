import string

import sublimeHelper

class CommentsWrite():

    def __init__(self, mem):
        self.gc = mem
        self.parser = self.gc.parser
        self.sublime = self.gc
        self.view = self.gc.view
        self.edit = self.gc.edit
        self.subHelp = sublimeHelper.SublimeHelper(mem)


    def writeComments(self, newDocBlock):
        self.removeOldDocBlocks(self.gc.matches)

        self.insertNewDocBlocks(newDocBlock, self.gc.matches, self.gc.indent)

    def insertNewDocBlocks(self, newDocBlock, matches, indent):
        if len(matches):
            rowInsert = matches.pop()['row']
        else:
            rowInsert = self.findInsertRow()

        self.subHelp.positionCursor(rowInsert - 1)

        if newDocBlock:
            self.subHelp.insertNewLine()

        indentedDocBlock = self.indentDocBlock(newDocBlock, indent)

        self.subHelp.insertSnippet(indentedDocBlock)

        linesAdded = indentedDocBlock.count("\n")
        if 0 < linesAdded:
            self.gc.currentFnRow += linesAdded + 1

    def removeOldDocBlocks(self, matches):
        """Delete all lines containing docBlocs and insert new
            ones at first line of old docBlocks"""
        for v in matches:
            self.subHelp.removeLine(v['row'] - 1)
            # Substract from the current fn pos as lines above it are removed
            self.gc.currentFnRow -= 1


    def indentDocBlock(self, docBlock, indent):
        indentedDocBlock = []
        for v in docBlock:
            indentedDocBlock.append(indent + ' ' + v)

        return string.join(indentedDocBlock, "\n")

    def findInsertRow(self):
        """Return the row to start inserting the new DocBlock"""

        docBlockCoords = self.gc.docBlockCoords

        if docBlockCoords['lastAtFound']:
            return docBlockCoords['lastAtFound']


        # Check for same line cases (inline)
        if docBlockCoords['docBlockStart'] == docBlockCoords['docBlockEnd']:
            return docBlockCoords['docBlockStart'] + 2

        return docBlockCoords['docBlockEnd']
