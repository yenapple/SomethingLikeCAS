import copy
import functools
import math
from collections import defaultdict

#부동 소수점 문제 조속히 해결 바람.


def Sigma(*args):
    sp = args[0]
    for x in range(1, len(args)):
        sp += args[x]
    return sp

def Product(*args):
    sp = args[0]
    for x in range(1, len(args)):
        sp *= args[x]
    return sp


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

    def __init__(self, char, tool = None):

        self.Name = char
        self.Evaluation = tool # numerical function used to actual evaluation.

    def __eq__(self, other):

        return self.Name == other.Name

# Built - in Operator instances. Only x and + takes multiple operands, which is import.
ADD = Operator("+", Sigma)
MUL = Operator("*", Product)
POW = Operator("^", pow)
DIV = Operator("/", lambda x, y: x/y)
NEG = Operator("-", lambda x: -x) # Is it more natural to use NEG function separately? or...
COS = Operator("COS", math.cos)
SIN = Operator("SIN", math.sin)
LN = Operator("LN", lambda x: math.log(x, math.e))
DEL = Operator("DEL", lambda x: 0)

class Function: # Function class
    # should be designed primarily by two important and distinct category of functions and <Unitary Functions>
    UnitaryNames = [ "SIN", "COS", "NEG", "LN", "Const" "Identity"]

    def __init__(self, parameters =(), operator = Operator(""), *operands):

        self.Parameters = parameters
        self.Operator = operator
        self.Operands = list(operands)

        self.Name = None
        self.Value = None

        self.Type = None # Type attribute.
        self.InverseImage = None # Isomorphic object in specific family of functions


    def __call__(self, call_option = False, *args):

        if len(args) != len(self.Parameters):
            print(len(args))
            return "Fuck You"
        elif args == self.Parameters: # Default call optimization f(Parameters).
            return self

        elif self == Neg and len(args) == 1 and isinstance(args[0], ConstantMap): # -0 is 0.
            return ConstantMap(-(args[0].Value))
        elif self == Neg and len(args) == 1 and args[0].Type == "Polynomial_single":
            #Monomorphism code.
            return (args[0].InverseImage.Scale(-1)).ConvertToFunction(args[0].Parameters[0])
        else:
            substitution_table = defaultdict(list,dict(zip([i.Name for i in self.Parameters], args)))
            #print(substitution_table)
            clone = copy.deepcopy(self)
            Substitute(clone, substitution_table)

        if call_option: # False if not explicitly given parameter order

            redefined_parameters = (IdentityMap(i) for i in call_option)
        else:
            redefined_parameters = tuple(set(functools.reduce(lambda x,y : x + y , (i.Parameters for i in args))))

        if IsConst(clone):
            return EvaluateConst(clone)
        else:
            setattr(clone, 'Parameters', redefined_parameters)
        return clone



    def __eq__(self, other): # Merely comparing two function by =. this is "For developer" function.

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return self.Value == other.Value

        #Monomorphism code.
        if self.Type == "Polynomial_single"and other.Type == "Polynomial_single" and self.Parameters == other.Parameters:
            return self.InverseImage == other.InverseImage

        return self.Operator == other.Operator and self.Operands == other.Operands
        #같은 것은 같은 것이므로 패러미터는 비교하지 않는다.

    def __add__(self, other):

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return ConstantMap(self.Value + other.Value)

        #Monomorphism code.
        if self.Type == "Polynomial_single"and other.Type == "Polynomial_single" and self.Parameters == other.Parameters:
            print('here')
            return (self.InverseImage + other.InverseImage).ConvertToFunction(self.Parameters[0])


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

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return ConstantMap(self.Value * other.Value)

        #Monomorphism code.
        if self.Type == "Polynomial_single" and other.Type == "Polynomial_single" and self.Parameters == other.Parameters:
            return (self.InverseImage * other.InverseImage).ConvertToFunction(self.Parameters[0])

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
            return self + Neg(False, other)


    def __pow__(self, other):

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return ConstantMap(pow(self.Value, other.Value))


        #여기서는 Isomorphism code 의 사용에 대해 주의가 필요하다. 이것은 representation 에 대한 논의 후로 미룬다.
        #Basic simplification
        if self == ONE:
            return self
        elif other == ZERO: # Tradition : 0^0 = 1.
            return ONE
        else:
            redefined_parameters = tuple(set(self.Parameters + other.Parameters))

            return Function(redefined_parameters, POW, copy.deepcopy(self), copy.deepcopy(other))



    def __truediv__(self, other):

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return ConstantMap(self.Value/other.Value)

        if other == ZERO:
            raise ZeroDivisionError
        elif self == other:
            return ONE
        else:
            redefined_parameters = tuple(set(self.Parameters + other.Parameters))

            return Function(redefined_parameters, DIV, copy.deepcopy(self), copy.deepcopy(other))


    def IsUnitary(self): #Unitary Function Check
        return self.Operator.Name in Function.UnitaryNames

    def IsEquivalent(self): # Beta Reduction Equivalency. This needs more discussion.
        pass


class ConstantMap(Function): # Used for 'Numbers'

    def __init__(self, value):

        Function.__init__(self, (), Operator("Const"), self)
        self.Value = value

    def __call__(self, call_option = False, *args):

        return self

    def __str__(self):
        return str(self.Value)

    # Constant 의 패러미터는 기본적으로 없다. 다만 직접 정의할 수는 있다. :f(x) = 3 과 같다. 그러나 그것은 미분과 __eq__에서는 여느 상수와 같이 취급되게 된다.
    # 그러니까, 패러미터 있는 상수나 패러미터 없는 상수나 사실 똑같게 처리해야 한다.

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

    def __call__(self, call_option = False, *args):

        if len(args)!=1:
            return "Fuck You"

        return args[0]

    def __str__(self):
        return self.Name


# Lemma Code
def Substitute(function, substitution_table):

    ops = function.Operands

    for x in range(len(ops)):

        if isinstance(ops[x], IdentityMap):
            name = ops[x].Name
            arg = substitution_table[name]
            if not arg:
                pass
            else:
                ops[x] = arg

        elif isinstance(ops[x], ConstantMap):
            pass

        else:
            Substitute(ops[x], substitution_table)

def IsConst(function): # to check a function is "actually" constant.
    if isinstance(function, ConstantMap):
        return True

    elif isinstance(function, IdentityMap):
        return False

    else:
        ops = function.Operands
        temp = True
        for x in range(len(ops)):
            temp = temp * IsConst(ops[x])

        return temp

#기본형은 위와 같으나, cos^2(x) + sin^2(x) 등을 상수로 인식하기 위해서는 다른 단순화법 -예를 들면  "미분해서 0" 같은 것이 필요하다.
# 미분은 조금 이따 만들 예정이므로 이 부분은 일단 작성하지 않아 보자.

def EvaluateConst(const_tree): # Evaluating real value of Constant Tree.
    if isinstance(const_tree, ConstantMap):
        return const_tree
    else:
        op = const_tree.Operator
        if not const_tree.IsUnitary(): #Unitary 하지 않은 연산자일 경우의 처리방식
            return op.Evaluation(*[EvaluateConst(i) for i in const_tree.Operands])
        else: #Unitary 할 경우에는 처리방식이 조금(!) 다르다.
            return ConstantMap(op.Evaluation(EvaluateConst(const_tree.Operands[0]).Value))




# Fundamental Constants used frequently.
ONE = ConstantMap(1)
ZERO = ConstantMap(0)
PI = ConstantMap(math.pi)
E = ConstantMap(math.e)

# Fundamental Variable X used for built - in Unitary Functions.
VarX = IdentityMap("x")
VarY = IdentityMap("y")
VarZ = IdentityMap("z")

# Four basic Built - in Functions.
Neg = Function((VarX,), NEG, VarX)
Sin = Function((VarX,), SIN, VarX)
Cos = Function((VarX,), COS, VarX)
Ln = Function((VarX,), LN, VarX)
Log = Ln(False, VarX)/Ln(False, VarY) # Log_x(y). this needs more discussion.



#Single variable polynomial processing class----------------------------------------------------------------------------
class Polynomial:

    def __init__(self, coefficients):

        self.Coefficients = Trim_list(coefficients)
        self.Degree = len(self.Coefficients)-1

    # x would be representing single variable here.
    def __str__(self):
        temp = [str(self.Coefficients[i]) + "x^" + str(self.Degree - i) + "+" for i in range(self.Degree + 1)]
        string = ''
        for x in range(len(temp)):
            string +=temp[x]
        return string[:-4]

    def __eq__(self, other):
        return self.Coefficients == other.Coefficients

    def __add__(self, other):

        s, o = self.Coefficients, other.Coefficients

        if self.Degree == other.Degree:
            pass
        elif self.Degree > other.Degree:
            o = Pad_list(o, self.Degree - other.Degree, "L")
        else:
            s = Pad_list(s, other.Degree - self.Degree, "L")

        a = (lambda x, y: [x[n] + y[n] for n in range(len(x))])(s, o)
        return Polynomial(a)

    # Scalar multiple
    def Scale(self, c):

        a = (lambda x, y: [y*x[n] for n in range(len(x))])(self.Coefficients, c)
        return Polynomial(a)

    def __sub__(self, other):
        return self + other.Scale(-1)

    def __mul__(self, other):

        s, o = Pad_list(self.Coefficients, other.Degree, "L"), Pad_list(other.Coefficients, self.Degree, "L")
        s.reverse()
        o.reverse()

        # Cauchy Product.
        a = [sum([s[x] * o[k - x] for x in range(k+1)]) for k in range(self.Degree + other.Degree+1)]
        a.reverse()
        return Polynomial(a)

    #"quotient".
    def Quotient_div(self, other):
        if other == Polynomial([0]):
            raise ZeroDivisionError
        else:
            if self.Degree < other.Degree:
                return Polynomial([0])

            elif self.Degree == other.Degree:
                q = self.Coefficients[0]/other.Coefficients[0]
                return Polynomial([q])
            else:
                q = self.Coefficients[0]/other.Coefficients[0]
                q1 = (Polynomial(Pad_list([1], self.Degree - other.Degree, "R")).Scale(q))
                r1 = self - q1 * other
                return q1 + r1.Quotient_div(other)

    def __divmod__(self, other):

        quotient = self.Quotient_div(other)
        remainder = self - quotient * other
        return quotient, remainder

    def Pow_int(self, n):

        if n < 0 or n != n//1:
            return "Not closed under this operation"

        elif n == 0:
            return Polynomial([1])
        else:
            return self * self.Pow_int(n-1)

    def Differentiate(self):

        ary = Dot(self.Coefficients, [self.Degree - n for n in range(self.Degree + 1)])
        del ary[-1]
        return Polynomial(ary)

    # Evaluating polynomial function "self" indicates.
    def Evaluate(self, x):
        return sum([self.Coefficients[n]*pow(x, self.Degree - n) for n in range(self.Degree+1)])

    def ConvertToFunction(self, parameter):
        #Monomorphism: Polynomial -> Function.

        summation = [ConstantMap(self.Coefficients[i]) * pow(parameter, ConstantMap(self.Degree - i))  for i in range(self.Degree + 1)]
        a = Function((parameter,) , ADD, *summation)
        setattr(a, "Type", "Polynomial_single")
        setattr(a, "InverseImage", self)
        return a


# (x - p) 진법으로 다항식을 나타내 주는 함수.

def X_P_base(polynomial, p):
    n = 0
    base = Polynomial([1, -p])
    result = []

    d = polynomial
    while n != (polynomial.Degree+1):
        t = divmod(d, base)
        result.append(t[1])
        d = t[0]
        n = n + 1

    result.reverse()
    return result




#lemma codes---------------------------------------
def Trim_list(ary):
    if not ary:
        raise IndexError
    else:
        while ary[0] == 0:
            del ary[0]
            if not ary:
                return [0]
        else:
            return ary

def Pad_list(ary, n, direction):
    if direction == "L":
        return [0 for x in range(n)] + ary
    elif direction == "R":
        return ary + [0 for x in range(n)]
    else:
        return "Fuck You"


def Dot(ary1, ary2):
    if len(ary1) != len(ary2):
        return IndexError
    else:
        return [ary1[n] * ary2[n] for n in range(len(ary1))]





#p = Polynomial([1,2,1])
#P_x = p.ConvertToFunction(VarX)
#Q_x = p.ConvertToFunction(VarX)

#R = P_x * Q_x
