import re


regFunc = re.compile(r"([^\s]\w+)?[\s\t]*([^\w]?)(function)[\s\t]*([\W]*)[\s\t]*([\w]*)", re.I)

regFuncExpression = re.compile(r"^[\s\t]*[\'\"a-zA-Z_]{1}[\w\.]*[\'\s\t]*[\:\=]{1}[\s\t]*function", re.I)

regFuncDeclaration = re.compile(r"^[\s\t]*function[\s\t]+[a-zA-Z_]{1}[\w]*", re.I)

def enum(**enums): return type('Enum', (), enums)

# Define the JS function types
FuncType = enum(
    NEW_FUNC=1,
    EXPRESSION=2,
    DECLARATION=3,
    ANON=4
    )


def getFuncType(funcLine):
    """-DOES NOT WORK- regex is good though
        Return the function type in the provided funcLine
        will return None if no match was found
    """
    res = regFunc.search(funcLine)
    if not res: return None

    if not isinstance(res.groups(), tuple): return None

    # Func is at start of line
    SOL = False
    # Func is at end of line
    EOL = False


    prefix = str(res.group(1))
    attached_prefix = str(res.group(2))
    attached_suffix = str(res.group(4))
    suffix = str(res.group(5))

    if res.group(1) is None: SOL = True
    if "" == suffix: EOL = True

    out = prefix + '::' + attached_prefix + '::' + attached_suffix + '::' + suffix + '::' + str(SOL) + '::' + str(EOL)

    return out

def properFunc(funcLine):
    """Return boolean if function statement is ok to work on
        We consider proper funcs if they are of the format:
        function aDeclaration(){}
        an.expression.func = function(){}
        'keyInAnObject' : function() {}
        keyInAnObject : function(){}
    """
    if regFuncExpression.match(funcLine): return True

    # test for declaration
    if regFuncDeclaration.match(funcLine): return True
    return False



#anon = "this.el.$modalWelcomeBtn.on('click', goog.bind(Function(){}, this));"
anon = "zit.forEach(function zitForEach(item){"
print properFunc(anon)
