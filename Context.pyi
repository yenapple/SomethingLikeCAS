import copy
import functools
import math

Context_space = [] # Existing Contexts

CurrentContext = None # Now using Context


def Run(): # User Interface to execute on certain context
    pass

def Close_context():
    global CurrentContext
    CurrentContext = None


class Context: # class of Contexts

    def __init__(self):

        global Context_space
        self.namespace = []
        Context_space.append(self)

    def load(self):

        global CurrentContext
        CurrentContext = self


# 많은 단순화를 파서가 알아서 다 해줍니다.^^ "여기서는 연산에서의 단순화만 적용하면 됩니다."
# 그래도 최종 단순화 루틴을 짜긴 짜야 할 거 같다. 파싱을 똑똑하게 해놓고 트리를 만든 상태에서 단순화를 해야 유리한 패턴도 분명 있다.

#Functional Structure Code ---------------------------------------------------------------------------------------------------------------------------------

class Operator: #Operator class

    Names = ["", "+", "x", "^", "/", "DEL", "LN", "SIN", "COS", "NEG", "Const" "Identity"]

    def __init__(self, char):

        self.Name = char

    def __eq__(self, other):

        return self.Name == other.Name

# Built - in Operator instances
ADD = Operator("+")
MUL = Operator("*")
POW = Operator("^")
DIV = Operator("/")
NEG = Operator("-") # Is it more natural to use NEG function separately? or...
COS = Operator("COS")
SIN = Operator("SIN")
LN = Operator("LN")
DEL = Operator("DEL")

class Function: # Function class
    # should be designed primarily by two important and distinct category of functions and <Unitary Functions>
    UnitaryNames = [ "SIN", "COS", "NEG", "LN", "Const" "Identity"]

    def __init__(self, parameters =(), operator = Operator(""), *operands):

        self.Parameters = parameters
        self.Operator = operator
        self.Operands = list(operands)


    def __call__(self, call_option, *args):

        if args == self.Parameters: # Default call optimization f(Parameters).
            return self

        if len(args) != len(self.Parameters):
            return "Fuck You"
        elif self == Neg and args ==(ZERO,): # -0 is 0.
            return ZERO
        else:
            substitution_table = dict(zip([i.Name for i in self.Parameters], args))
            clone = copy.deepcopy(self)
            Substitute(clone, substitution_table)

        if call_option: # False if not explicitly given parameter order

            redefined_parameters = (IdentityMap(i) for i in call_option)
        else:
            redefined_parameters = tuple(set(functools.reduce(lambda x,y : x + y , (i.Parameters for i in args))))

        setattr(clone, 'Parameters', redefined_parameters)

        return clone



    def __eq__(self, other): # Merely comparing two function by =. this is "For developer" function.

        return self.Operator == other.Operator and self.Operands == other.Operands

    def __add__(self, other):
        # Basic simplification
        if self == ZERO:
            return other
        elif other == ZERO:
            return self
        else:
            redefined_parameters = tuple(set(self.Parameters + other.Parameters))

            # Redundant parenthesis is not good for health.
            if self.Operator == ADD and other.Operator == ADD:
                return Function(redefined_parameters, ADD, *(copy.deepcopy(self.Operands) + copy.deepcopy(other.Operands)))
            elif self.Operator == ADD:
                return Function(redefined_parameters, ADD, *(copy.deepcopy(self.Operands) + [copy.deepcopy(other)]))
            elif other.Operator == ADD:
                return Function(redefined_parameters, ADD, *([copy.deepcopy(self)] + copy.deepcopy(other.Operands)))

            else:
                return Function(redefined_parameters, ADD, copy.deepcopy(self), copy.deepcopy(other))

    def __mul__(self, other):
        #Basic simplification
        if self == ONE:
            return other
        elif other == ONE:
            return self
        else:
            redefined_parameters = tuple(set(self.Parameters + other.Parameters))

            # Redundant parenthesis is not good for health.
            if self.Operator == MUL and other.Operator == MUL:
                return Function(redefined_parameters, MUL, *(copy.deepcopy(self.Operands) + copy.deepcopy(other.Operands)))
            elif self.Operator == MUL:
                return Function(redefined_parameters, MUL, *(copy.deepcopy(self.Operands) + [copy.deepcopy(other)]))
            elif other.Operator == MUL:
                return Function(redefined_parameters, MUL, *([copy.deepcopy(self)] + copy.deepcopy(other.Operands)))

            else:
                return Function(redefined_parameters, MUL, copy.deepcopy(self), copy.deepcopy(other))

    def __sub__(self, other):
        if self == other:
            return ZERO
        else:
            return self + Neg(other)

    def __pow__(self, other):
        #Basic simplification
        if self == ONE:
            return self
        elif other == ZERO: # Tradition : 0^0 = 1.
            return ONE
        else:
            redefined_parameters = tuple(set(self.Parameters + other.Parameters))

            return Function(redefined_parameters, POW, copy.deepcopy(self), copy.deepcopy(other))

    def __truediv__(self, other):
        #Basic simplification
        if other == ZERO:
            raise ZeroDivisionError
        elif self == other:
            return ONE
        else:
            redefined_parameters = tuple(set(self.Parameters + other.Parameters))

            return Function(redefined_parameters, DIV, copy.deepcopy(self), copy.deepcopy(other))


    def IsUnitary(self): #Unitary Function Check
        return self.Operator.Name in Function.UnitaryNames

    def IsEquivalent(self): # Beta Reduction Equivalency. Tree isomorphism.
        pass


class ConstantMap(Function): # Used for 'Numbers'

    def __init__(self, value):

        Function.__init__(self, (), Operator("Const"), self)
        self.Value = value

    def __eq__(self, other):

        return self.Value == other.Value

    def __add__(self, other):

        return ConstantMap(self.Value + other.Value)

    def __mul__(self, other):

        return ConstantMap(self.Value * other.Value)

    def __pow__(self, other):

        return ConstantMap(pow(self.Value, other.Value))

    def __truediv__(self, other):

        return ConstantMap(self.Value/other.Value)

    def __call__(self, call_option = 0, *args):

        return self


class IdentityMap(Function): # Identity map. Used for parametrization

    def __init__(self, letter):

        Function.__init__(self, (self,) , Operator("Identity"), self)
        self.Name = letter

    def __eq__(self, other):

        return self.Name == other.Name

    def __hash__(self):

        return ord(self.Name)

    #This code has to be discussed further to be justified. Do we need deepcopy for even identity map?
    #def __add__(self, other):

        #return Function(tuple({self, other}), Operator("+"), *(self, other)) for Operands part, ...

    #def __mul__(self, other):

        #return Function(tuple({self, other}), Operator("*"), *(self, other))

    def __call__(self, call_option, *args):

        if len(args)!=1:
            return "Fuck You"

        return args[0]


# Lemma Code

def Substitute(function, substitution_table):

    ops = function.Operands

    for x in range(len(ops)):

        if isinstance(ops[x], IdentityMap):
            name = ops[x].Name
            arg = substitution_table[name]
            ops[x] = arg

        elif isinstance(ops[x], ConstantMap):
            pass

        else:
            Substitute(ops[x], substitution_table)

# Fundamental Constants used frequently.
ONE = ConstantMap(1)
ZERO = ConstantMap(0)
PI = ConstantMap(math.pi)
E = ConstantMap(math.e)

# Fundamental Variable X used for built - in Unitary Functions.
VarX = IdentityMap("x")
VarY = IdentityMap("y")

# Four basic Built - in Functions.
Neg = Function((VarX,), NEG, VarX)
Sin = Function((VarX,), SIN, VarY)
Cos = Function((VarX,), COS, VarX)
Ln = Function((VarX,), LN, VarX)
Log = Ln(VarX)/Ln(VarY) # Log_x(y). this needs more discussion.


