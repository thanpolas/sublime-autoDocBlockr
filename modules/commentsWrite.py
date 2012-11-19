import string
import logging

import sublimeHelper

module_logger = logging.getLogger('autoDocBlockr.commentsWrite')


class CommentsWrite():

    def __init__(self, mem):
        self.log = logging.getLogger('autoDocBlockr.commentsWrite.CommentsWrite')
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
        rowInsert = self.findInsertRow()

        indentedDocBlock = self.indentDocBlock(newDocBlock, indent)
        if indentedDocBlock: indentedDocBlock += "\n"

        self.subHelp.insert(self.subHelp.getRowFirstPoint(rowInsert - 1, True), indentedDocBlock)

    def removeOldDocBlocks(self, matches):
        """Delete all lines containing docBlocs and insert new
            ones at first line of old docBlocks"""
        for v in reversed(matches):
            removeRow = v['row'] - 1
            removeRowsCount = max(1, v['line'].count("\n"))
            self.subHelp.removeLine(removeRow, removeRowsCount)


    def indentDocBlock(self, docBlock, indent):
        indentedDocBlock = []
        for v in docBlock:
            indentedDocBlock.append(indent + ' ' + v)

        return string.join(indentedDocBlock, "\n")

    def findInsertRow(self):
        """Return the row to start inserting the new DocBlock"""

        matchesLen = len(self.gc.matches)
        if matchesLen:
            return self.gc.matches[0]['row']

        docBlockCoords = self.gc.docBlockCoords
        if docBlockCoords['fistDocRow']:
            return docBlockCoords['fistDocRow']


        # Check for same line cases (inline)
        if docBlockCoords['docBlockStart'] == docBlockCoords['docBlockEnd']:
            return docBlockCoords['docBlockStart'] + 2

        return docBlockCoords['docBlockEnd']
