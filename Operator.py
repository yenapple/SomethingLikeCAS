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
class Operator:

    Names = ["", "+", "x", "^", "LN", "SIN", "COS", "Const" "Identity"]
    UnitaryNames = ["SIN", "COS", "LN", "Const" "Identity"]

    def __init__(self, char, evaluation_func=None):

        self.Name = char
        self.EvaluationFunction = evaluation_func

    def __eq__(self, other):

        return self.Name == other.Name


# Built - in Operator instances. Only x and + takes multiple operands, which is important.
ADD = Operator("+", Sigma)
MUL = Operator("*", Product)
POW = Operator("^", pow)
COS = Operator("COS", math.cos)
SIN = Operator("SIN", math.sin)
LN = Operator("LN", lambda x: math.log(x, math.e))
DEL = Operator("DEL", lambda x: 0)
CONST = Operator("CONST", )
IDENTITY = Operator("Identity")
