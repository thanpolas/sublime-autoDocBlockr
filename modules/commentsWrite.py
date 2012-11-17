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

        # Find the row insert will happen
        if len(matches):
            rowInsert = matches.pop()['row']
        else:
            rowInsert = self.findInsertRow()

        # self.subHelp.positionCursor(rowInsert - 1)

        indentedDocBlock = self.indentDocBlock(newDocBlock, indent)

        if indentedDocBlock: indentedDocBlock += "\n"

        #print matches
        #print self.subHelp.getRowFirstPoint(rowInsert - 1, True)
        #print indentedDocBlock
        #self.subHelp.insertSnippet(indentedDocBlock)
        self.subHelp.insert(self.subHelp.getRowFirstPoint(rowInsert - 1, True), indentedDocBlock)

        linesAdded = indentedDocBlock.count("\n")
        if 0 < linesAdded:
            self.gc.currentFnRow += linesAdded + 1

    def removeOldDocBlocks(self, matches):
        """Delete all lines containing docBlocs and insert new
            ones at first line of old docBlocks"""
        for v in reversed(matches):
            removeRow = v['row'] - 1
            removeRowsCount = max(1, v['line'].count("\n"))
            print "Param:" + v['paramName'] + ' row:' + str(removeRow) + ' rows:' + str(removeRowsCount)
            self.subHelp.removeLine(removeRow, removeRowsCount)
            # Substract from the current fn pos as lines above it are removed
            #self.gc.currentFnRow -= 1


    def indentDocBlock(self, docBlock, indent):
        indentedDocBlock = []
        for v in docBlock:
            indentedDocBlock.append(indent + ' ' + v)

        return string.join(indentedDocBlock, "\n")

    def findInsertRow(self):
        """Return the row to start inserting the new DocBlock"""

        docBlockCoords = self.gc.docBlockCoords
        if docBlockCoords['fistDocRow']:
            return docBlockCoords['fistDocRow']


        # Check for same line cases (inline)
        if docBlockCoords['docBlockStart'] == docBlockCoords['docBlockEnd']:
            return docBlockCoords['docBlockStart'] + 2

        return docBlockCoords['docBlockEnd']
