
import os


def syntax_name(view):
    syntax = os.path.basename(view.settings().get('syntax'))
    syntax = os.path.splitext(syntax)[0]
    return syntax

def checkSyntax(view, ignore_disabled=False):
    """Returns boolean, checks if file in supported file syntax"""
    syntax = syntax_name(view)
    lc_syntax = syntax.lower()
    language = None
    syntaxMap = view.settings().get('autoDocBlockr_syntax_map', {})
    if syntax in syntaxMap:
        language = syntax.lower()
    elif lc_syntax in syntaxMap:
        language = lc_syntax.lower()

    if language:
        return True
    return False
