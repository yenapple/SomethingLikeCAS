import copy
import functools

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




#Functional Structure Code ---------------------------------------------------------------------------------------------------------------------------------

class Operator: #Operator class

    Names = ["", "+", "x", "^", "/", "Del", "Log", "Sin", "Cos", "Neg", "Const" "Identity"]

    def __init__(self, char):

        self.Name = char

    def __eq__(self, other):

        return self.Name == other.Name







class Function: # Function class
    # should be designed primarily by two important and distinct category of functions and <Unitary Functions>

    def __init__(self, parameters =(), operator = Operator(""), *operands):

        self.Parameters = parameters
        self.Operator = operator
        self.Operands = operands


    def __call__(self, call_option, *args):

        if args == self.Parameters: # Default call optimization f(Parameters).
            return self

        if len(args) != len(self.Parameters):
            return "Fuck You"
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



    def __eq__(self, other): # Merely comparing two function by = . This needs more discussion: Tree isomorphism.
        pass

    def __add__(self, other):
        redefined_parameters = tuple(set(self.Parameters + other.Parameters))

        return Function(redefined_parameters, Operator("+"), copy.deepcopy(self), copy.deepcopy(other))

    def __mul__(self, other):
        redefined_parameters = tuple(set(self.Parameters + other.Parameters))

        return Function(redefined_parameters, Operator("*"), copy.deepcopy(self), copy.deepcopy(other))

    def IsUnitary(self): #Unitary Function Check
        return self.Operator.Name in ("Log", "Sin", "Cos", "Neg", "Const" "Identity")

    def IsEquivalent(self): # Beta Reduction Equivalency
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

    #This code has to be discussed further to be justified.
    #def __add__(self, other):

        #return Function(tuple({self, other}), Operator("+"), *(self, other))

    #def __mul__(self, other):

        #return Function(tuple({self, other}), Operator("*"), *(self, other))

    def __call__(self, call_option, *args):

        if len(args)!=1:
            return "Fuck You"

        return args[0]


# Lemma Code

def Substitute(function, substitution_table):

    ops = function.Operator

    for x in range(len(ops)):

        if isinstance(ops[x], IdentityMap):
            name = ops[x].Name
            arg = substitution_table[name]
            ops[x] = arg

        elif isinstance(ops[x], ConstantMap):
            pass

        else:
            Substitute(ops[x], substitution_table)

