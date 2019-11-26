import math

#lemma code
def Sigma(*args):
    sp = args[0]
    for x in range(1, len(args)):
        sp += args[x]
    return sp

#lemma code
def Product(*args):
    sp = args[0]
    for x in range(1, len(args)):
        sp *= args[x]
    return sp

def Print_list(lst):
    for i in lst:
        print(i)


class Operator:

    Names = ["", "+", "x", "^", "LN", "SIN", "COS", "ARS", "ARC", "ART", "Const" "Identity", "Del", "Default"]
    UnitaryNames = ["SIN", "COS", "LN", "ARS", "ARC", "ART" "Const" "Identity", "Default"]

    def __init__(self, char, evaluation_func=None):

        self.Name = char
        self.EvaluationFunction = evaluation_func
        self.Inverse = None


    def __eq__(self, other):

        return self.Name == other.Name

    def __hash__(self):
        return Operator.Names.index(self.Name)

    def __str__(self):
        return self.Name


# Built - in Operator instances. Only x and + takes multiple operands, which is important.
ADD = Operator("+", Sigma)
MUL = Operator("*", Product)
POW = Operator("^", pow)
COS = Operator("COS", math.cos)
SIN = Operator("SIN", math.sin)
ARCSIN = Operator("ARS", math.asin)
ARCCOS = Operator("ARC", math.acos)
ARCTAN = Operator("ART", math.atan)
LN = Operator("LN", lambda x: math.log(x, math.e))
DEL = Operator("Del", lambda x: 0)
CONST = Operator("Const", )
IDENTITY = Operator("Identity")
DEFAULT = Operator("Default")

setattr(SIN, "Inverse", ARCSIN)
setattr(COS, "Inverse", ARCCOS)
setattr(ARCSIN, "Inverse", SIN)
setattr(ARCCOS, "Inverse", COS)
