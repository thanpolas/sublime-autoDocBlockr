"""
    Will parse the Document Block comments and return a match dict
"""
import re
import string
import logging

import sublimeHelper

module_logger = logging.getLogger('autoDocBlockr.commentsParser')

def enum(**enums): return type('Enum', (), enums)

# Define the matchtypes enum
MatchTypes = enum(BOGUS=1, PARAM=2)


def getLastLine(parser, view, currentPoint):
    return parser.getDefinition(view, view.line(currentPoint).begin() - 1)


class CommentsParser():

    parser = None
    sublime = None
    view = None
    # Max times to look for docBlock lines from function
    maxTimes = 30
    # The regex for the start of the docblock
    regBlockStart = re.compile(r"^\s*(\/\*|###)\*$")
    # the regex to pull the param name
    regParamName = re.compile(r"^([\s|\t]*)(\*\s\@param\s*)([^\s|\t]+[\s|\t]*)([^\s][\w]+)")
    # Regex to track lines with any doc bloc (@anything)
    regAtFound = re.compile(r"([\s|\t]*)(\*\s\@\w*\s*)")

    def __init__(self, mem):
        self.log = logging.getLogger('autoDocBlockr.commentsParser.CommentsParser')
        self.gc = mem
        self.parser = self.gc.parser
        self.sublime = self.gc
        self.view = self.gc.view
        self.edit = self.gc.edit
        self.subhelp = sublimeHelper.SublimeHelper(self.gc)
        # The regex to match invalidated params
        invalidPrefix = mem.settings.get('autoDocBlockr_invalid_prefix')
        reInvalidParam = r"^([\s|\t]*)(\*\s"
        reInvalidParam += "\\" + invalidPrefix
        reInvalidParam += r"param\s*)([^\s|\t]+[\s|\t]*)([^\s][\w]+)"
        self.regInvalidParam = re.compile(reInvalidParam)
        self.log.info('Intialized')

    def parseComments(self, mem):
        """ Parse comments if no comments found return None """

        self.matches = []

        p = self.parser

        self.currentPoint = mem.cursorPoint
        itterLine = getLastLine(p, self.sublime.view, self.currentPoint)

        if not p.isExistingComment(itterLine):
            return None

        # Initialize docBlock coordinates
        self.docBlockCoords = {
            'firstAtFound': None, # Row of First '@' we found while crawling'
            'lastAtFound': None, # Row of Last '@' we found while crawling up the docBlock
            'docBlockStart': self.subhelp.getRow(self.currentPoint),
            'docBlockEnd': None, # Row Block ends
            'docBlockEndPoint': -1, # DocBlock end point
            'docBlockStartPoint': -1 # DocBlock start point
        }

        allLines = self._read_docBlock()
        if len(allLines):
            self.docBlockCoords['docBlockEnd']=allLines[len(allLines) - 1]['row']
        #print string.join(allLines, "\n")
        self._parse_dockBlock(allLines)


        mem.docBlockCoords = self.docBlockCoords

        #print string.join([v["line"] for v in self.matches], "\n")
        return self.matches

    def _read_docBlock(self):
        """Return a list with all the document block lines"""
        allLines = []
        foundDocBlockStart = False
        for i in range(0, self.maxTimes):
            self.currentPoint -= 1
            self.currentPoint = self.sublime.view.line(self.currentPoint).begin()
            itterLine = getLastLine(self.parser, self.sublime.view, self.currentPoint)

            allLines.insert(0, {
                "currentPoint": self.currentPoint,
                "line": itterLine,
                "row": self.subhelp.getRow(self.currentPoint)
                })

            if self.regBlockStart.match(itterLine):
                self.docBlockCoords['docBlockStart']=self.subhelp.getRow(self.currentPoint)
                foundDocBlockStart=True
                break

        if not foundDocBlockStart: return None
        return allLines

    def _writeParamBuf(self, itterObj):
        itterObj['foundParam']=False
        itterObj['seq'] += 1

        self.writeMatch(MatchTypes.PARAM, itterObj['currentParamBuf'], itterObj['seq'], itterObj['paramName'])
        itterObj['paramName']=''
        itterObj['currentParamBuf']=[]

    def _parse_dockBlock(self, allLines):
        foundAnyParam=False

        itterObj = {
            'foundParam':False,
            'paramName':'',
            'currentParamBuf':[],
            'seq':0
        }
        for index, lineDict in enumerate(allLines):
            # Check if at last line
            if index == len(allLines) - 1 and itterObj['foundParam']: self._writeParamBuf(itterObj)


            # check if there's a doc on this line (@)
            # or an invalidated param (!param)
            if (self.regAtFound.match(lineDict["line"]) or
                    self.regInvalidParam.match(lineDict["line"])):
                if not foundAnyParam:
                    self.docBlockCoords["fistDocRow"]=lineDict["row"]
                    foundAnyParam=True

                if itterObj['foundParam']: self._writeParamBuf(itterObj)

                itterObj['paramName']=''

            res = self.regParamName.match(lineDict["line"])

            if not res:
                if itterObj['foundParam']:
                    itterObj['currentParamBuf'].append(lineDict)
                continue

            # A @param was found, see if there was a buffer open
            # and write param buffer to match array
            if itterObj['foundParam']:
                self._writeParamBuf(itterObj)

            if not isinstance(res.groups(), tuple):
                self.writeMatch(MatchTypes.BOGUS, [lineDict], itterObj['seq'])
                continue

            try:
                res.group(4)
            except:
                self.writeMatch(MatchTypes.BOGUS, [lineDict], itterObj['seq'])
                continue

            itterObj['foundParam']=True
            itterObj['paramName']=str(res.group(4))
            itterObj['currentParamBuf'].append(lineDict)

    def writeMatch(self, matchType, listLineDict, seq, paramName=''):
        """Create the match dict and append it to self.matches"""

        currentPoint=listLineDict[0]['currentPoint']
        row=self.subhelp.getRow(currentPoint)
        line=string.join([v["line"] for v in listLineDict], "\n")


        self.matches.append({
            'seq'      : seq,
            'matchType': matchType,
            'row'      : row,
            'paramName': paramName,
            'line'     : line #.replace('$', '\$').replace('{', '\{').replace('}', '\}')
            })
