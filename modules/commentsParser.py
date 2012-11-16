"""
    Will parse the Document Block comments and return a match dict
"""
import re

import sublimeHelper

def enum(**enums): return type('Enum', (), enums)

# Define the matchtypes enum
MatchTypes = enum(BOGUS=1, PARAM=2)


def getLastLine(parser, view, currentPoint):
    return parser.getDefinition(view, view.line(currentPoint).begin() - 1)


class CommentsParser():

    parser = None
    sublime = None
    view = None

    def __init__(self, mem):
        self.gc = mem
        self.parser = self.gc.parser
        self.sublime = self.gc
        self.view = self.gc.view
        self.edit = self.gc.edit
        self.subhelp = sublimeHelper.SublimeHelper(self.gc)

    def parseComments(self, mem):
        """ Parse comments if no comments found return None """






        matches = []
        reCommentsBlockStart = r"^\s*(\/\*|###)\*$"
        # the regex to pull the param name
        reCommentsParamName = r"^([\s|\t]*)(\*\s\@param\s*)([^\s|\t]+[\s|\t]*)([^\s][\w]+)"
        # Regex to track lines with any doc bloc (@anything)
        reCommentsDocBlocks = r"([\s|\t]*)(\*\s\@\w*\s*)"


        p = self.parser

        maxTimes = 30

        def writeMatch(matchType, itterLine, currentPoint, res):
            """ Append a dict with match info """

            row = self.subhelp.getRow(currentPoint)

            if MatchTypes.PARAM == matchType:
                paramName = str(res.group(4))
                col = res.start(4)
            else:
                paramName = ''
                col = None

            matches.append({
                'matchType': matchType,
                'row'      : row,
                'col'      : col,
                'paramName': paramName,
                'line'     : itterLine.replace('$', '\$').replace('{', '\{').replace('}', '\}')
                })

        currentPoint = mem.cursorPoint
        itterLine = getLastLine(p, self.sublime.view, currentPoint)

        if not p.isExistingComment(itterLine):
            return None

        # move backwards in lines and parse the docs until the
        # docs beginning is found, up to a max of 'maxTimes'

        regBlockStart = re.compile(reCommentsBlockStart)
        regParamName = re.compile(reCommentsParamName)
        regAtFoung = re.compile(reCommentsDocBlocks)

        docBlockCoords = {
            'lastAtFound': None, # Last '@' we found while crawling up the docBlock
            'docBlockStart': None, # Line the docblock starts from
            'docBlockEnd': self.subhelp.getRow(currentPoint)
        }
        for i in range(0, maxTimes):
            currentPoint -= 1
            currentPoint = self.sublime.view.line(currentPoint).begin()
            itterLine = getLastLine(p, self.sublime.view, currentPoint)

            if regBlockStart.match(itterLine):
                docBlockCoords['docBlockStart']=self.subhelp.getRow(currentPoint)
                break

            if regAtFoung.match(itterLine):
                docBlockCoords['lastAtFound']= self.subhelp.getRow(currentPoint)

            res = regParamName.match(itterLine)
            if res:
                matched = res.groups()
                if not isinstance(matched, tuple):
                    writeMatch(MatchTypes.BOGUS, itterLine, currentPoint, res)
                    continue
                try:
                    res.group(4)
                except:
                    writeMatch(MatchTypes.BOGUS, itterLine, currentPoint, res)
                    continue

                writeMatch(MatchTypes.PARAM, itterLine, currentPoint, res)

        mem.docBlockCoords = docBlockCoords

        # matches are written in reverse, decorate with a seq
        i = 0
        for v in reversed(matches):
            v['seq'] = i
            i += 1

        return matches

