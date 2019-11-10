import copy
import functools
import math
from collections import defaultdict
import Operator as Op
import Polynomial


class Function: # Function class
    # should be designed primarily by two important and distinct category of functions and <Unitary Functions>

    def __init__(self, parameters =(), operator = Op.Operator(""), *operands):

        self.Parameters = parameters
        self.Operator = operator
        self.Operands = list(operands)

        self.Name = None # 이 부분은 함수 자체의 이름으로 지어줘야 한다. User 단계니까 일단 패스.
        self.Value = None


    def __call__(self, call_option = False, *args):

        if len(args) != len(self.Parameters): #Funcking false call
            return "Fuck You"
        elif args == self.Parameters: # Default call optimization f(Parameters).
            return self
        else:
            redefined_parameters = Redefine_Parameter(call_option, *args)

            substitution_table = defaultdict(list,dict(zip([i.Name for i in self.Parameters], args)))
            clone = copy.deepcopy(self)
            Substitute(clone, substitution_table)

            # 치환된 것을 Top - down 방식으로 다시 계산하며 축약.
            clone = CalculateTree(clone)

            if isinstance(clone, ConstantMap):
                pass
            else:
                setattr(clone, 'Parameters', redefined_parameters)
            return clone

    def __eq__(self, other): # Merely comparing two function by =. this is "For developer" function.

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return self.Value == other.Value

        return self.Operator == other.Operator and self.Operands == other.Operands
        #같은 것은 같은 것이므로 패러미터는 비교하지 않는다.

    def __add__(self, other):

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return ConstantMap(self.Value + other.Value)
        else:
            f = Remove_Parenthesis(Op.ADD, self, other)
            f = Order_operands(f)
            f = Group_operands(f)
            return f

    #Syntactic sugar
    def __sub__(self, other):
        if self == other:
            return ZERO
        else:
            return self + NEG_ONE*other

    def __mul__(self, other):

        if isinstance(self, ConstantMap) and isinstance(other, ConstantMap):
            return ConstantMap(self.Value * other.Value)
        else:
            f = Remove_Parenthesis(Op.MUL, self, other)
            f = Order_operands(f)
            f = Group_operands(f)
            return f

    def __pow__(self, power, modulo=None):

        if isinstance(self, ConstantMap) and isinstance(power, ConstantMap):
            return ConstantMap(pow(self.Value, power.Value))
        else:
            f = Remove_Parenthesis(Op.POW, self, power)
            f = Order_operands(f)
            f = Group_operands(f)
            return f

    #Syntactic sugar
    def __truediv__(self, other):
        if other == ZERO:
            return ZeroDivisionError
        elif self == ZERO:
            return ZERO
        elif self == other:
            return ONE
        else:
            return self * pow(other, NEG_ONE)



    def Del(self, other): #Differentiation.
        # Del 의 처리는 쉽다. 그러나 이 operator 를 무슨 종류로 classify 해야 할까? Unitary Function?
        pass

    def IsUnitary(self):

        return self.Operator.Name in Op.Operator.UnitaryNames

class ConstantMap(Function): # Used for 'Numbers'

    def __init__(self, value):

        Function.__init__(self, (), Op.CONST, self)
        self.Value = value

    def __call__(self, call_option = False, *args):

        return self

    def __str__(self):
        return str(self.Value)

class IdentityMap(Function): # Identity map. Used for parametrization

    def __init__(self, letter):

        Function.__init__(self, (self,) , Op.IDENTITY, self)
        self.Name = letter

    def __eq__(self, other):

        return self.Name == other.Name

    # Warning: 이 코드는 본질을 흐린다. Function class 의 비교에는 사실 등식 밖에 없다. 부등호들은 편의상 도입한 것이며 실제 부등식 기능과는 관련이 없다.
    # 이것들은 인자의 우선 순위를 나타내는 것으로, ascii 비교의 정반대: x 가 y 보다 우선한다.
    def __gt__(self, other):

        return self.Name < other.Name

    def __lt__(self, other):

        return self.Name > other.Name

    def __hash__(self):

        return ord(self.Name)

    def __call__(self, call_option = False, *args):

        if len(args)!=1:
            return "Fuck You"

        return args[0]

    def __str__(self):

        return self.Name

# lemma code.
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

#lemma code
def IsConst(function, reference = ()):
    # reference X -> To check if it is literally constant
    # reference O -> To check if it is constant with respect to reference variables

    if isinstance(function, ConstantMap):
        return True

    elif isinstance(function, IdentityMap):
        if not reference:
            return False
        else:
            if function in reference:
                return False
            else:
                return True

    else:
        ops = function.Operands
        for x in range(len(ops)):
            if not IsConst(ops[x]):
                return False
            else:
                pass

        return True

#lemma code
def EvaluateConst(const_tree): # Evaluating real value of Constant Tree.

    if isinstance(const_tree, ConstantMap):
        return const_tree
    else:
        op = const_tree.Operator
        if not const_tree.IsUnitary():
            return op.EvaluationFunction(*[EvaluateConst(i) for i in const_tree.Operands])

        else:
            return ConstantMap(op.EvaluationFunction(EvaluateConst(const_tree.Operands[0]).Value))

#lemma code
def CalculateTree(function):
        if IsConst(function):
            return EvaluateConst(function)
        elif function.IsUnitary():
            return Function(function.Operator, CalculateTree(function.Operands[0]))
        else:
            op = function.Operator
            if op == Op.ADD:
                return Op.Sigma(*[CalculateTree(elem) for elem in function.Operands])
            elif op == Op.MUL:
                return Op.Product(*[CalculateTree(elem) for elem in function.Operands])
            elif op == Op.POW:
                return pow(CalculateTree(function.Operands[0]), CalculateTree(function.Operands[1]))

            # Should add Unitary Function - related simplification rule here. like sin^2 + cos^2 = 1..
'''
#lemma code
def IsPolynomial(function):

    if isinstance(function, ConstantMap):
        return True
    elif isinstance(function, IdentityMap):
        return True
    elif function.Operator.IsUnitary():
        return False

    else:
        ops = function.Operands
        for x in range(len(ops)):
            if not IsPolynomial(ops[x]):
                return False
            else:
                pass
        return True
'''


# Fundamental Variable X used for built - in Unitary Functions.
VarX = IdentityMap("x")
VarY = IdentityMap("y")
VarZ = IdentityMap("z")

# Four basic Built - in Functions.
Sin = Function((VarX,), Op.SIN, VarX)
Cos = Function((VarX,), Op.COS, VarX)
Ln = Function((VarX,), Op.LN, VarX)
Log = Ln(False, VarX)/Ln(False, VarY) # Log_x(y). this needs more discussion.

# Fundamental Constants used frequently.
ONE = ConstantMap(1)
NEG_ONE = ConstantMap(-1)
ZERO = ConstantMap(0)
PI = ConstantMap(math.pi)
E = ConstantMap(math.e)


#lemma code.
def Redefine_Parameter(call_option = False, *function_set):

        if call_option: # False if not explicitly given parameter order
            redefined_parameters = (IdentityMap(i) for i in call_option)

        else:
            redefined_parameters = tuple(set(functools.reduce(lambda x,y : x + y , (i.Parameters for i in function_set))))

        return redefined_parameters


#lemma code
def Remove_Parenthesis(operator, function1, function2):

        redefined_parameters = Redefine_Parameter(False, function1, function2)
        parenthesis_removed_form = ZERO

        if operator == Op.ADD or operator == Op.MUL:
            if function1.Operator == operator and function2.Operator == operator:
                parenthesis_removed_form = Function(redefined_parameters, operator, *(copy.deepcopy(function1.Operands) + copy.deepcopy(function2.Operands)))
            elif function1.Operator == operator:
                parenthesis_removed_form = Function(redefined_parameters, operator, *(copy.deepcopy(function1.Operands) + [copy.deepcopy(function2)]))
            elif function2.Operator == operator:
                parenthesis_removed_form = Function(redefined_parameters, operator, *([copy.deepcopy(function1)] + copy.deepcopy(function2.Operands)))
            else:
                pass

        elif operator == Op.POW:
            if function1.Operator ==  operator:
                parenthesis_removed_form = Function(redefined_parameters, operator, function1.Operands[0] * function2)


        parenthesis_removed_form = Function(redefined_parameters, operator, copy.deepcopy(function1), copy.deepcopy(function2))

        return parenthesis_removed_form

#lemma code
def Order_operands(function):

    if function.Operator == Op.POW:
        if function.Operands[0] == ONE or function.Operands[1] == ZERO:
            return ONE
        elif function.Operands[0] == ZERO:
            return ZERO
        elif function.Operands[1] == ONE:
            return function.Operands[0]
        else:
            return function

    elif function.Operator == Op.ADD or function.Operator == Op.MUL:

        constant_operands = [elem for elem in function.Operands if IsConst(elem)]
        non_constant_operands = [elem for elem in function.Opoerands if not elem in constant_operands]

        pre = function.Operator.EvaluationFunction(*constant_operands)
        temp = non_constant_operands

        if function.Operator == Op.ADD:
            if pre == ZERO:
                function.Operands = []
            else:
                function.Operands = [pre,]
                pass
        elif function.Operator == Op.MUL:
            if pre == ZERO:
                return ZERO
            elif pre == ONE:
                function.Operands = []
            else:
                function.Operands = [pre,]
                pass

        identity_operands = [elem for elem in temp if isinstance(elem, IdentityMap)]
        others = [elem for elem in temp if (elem not in identity_operands)]
        temp = sorted(identity_operands) + others

        function.Operands += temp

        if len(function.Operands) == 1:
            return function.Operands[0]
        else:
            return function
    else:
        return function

#lemma code.
def Group_operands(function):

    # For Only 2 multiplied terms
    if function.Operator == Op.ADD:
        lefts = []
        for elem in function.Operands:
            if elem.Operator == Op.MUL and len(elem.Operands) == 2:
                #Identity Map takes priority 1st.
                if isinstance(elem.Operands[0], IdentityMap) and isinstance(elem.Operands[0], IdentityMap):
                    lefts.append((max(elem.Operands), min(elem.Operands)))
                elif isinstance(elem.Operands[0], IdentityMap):
                    lefts.append((elem.Operands[0], elem.Operands[1]))
                elif isinstance(elem.Operands[1], IdentityMap):
                    lefts.append((elem.Operands[1], elem.Operands[0]))
                #And Unitary Functions.
                elif elem.Operands[0].IsUnitary() and not elem.Operands[1].IsUnitary():
                    lefts.append((elem.Operands[0], elem.Operands[1]))
                elif elem.Operands[1].IsUnitary() and not elem.Operands[0].IsUnitary():
                    lefts.append((elem.Operands[1], elem.Operands[0]))
                # Here, I 'd like to add ln(a) + ln(b) = ln(a*b). But this needs more discussion.
                else:
                    lefts.append((elem, ONE))
            else:
                lefts.append((elem, ONE))

        grouped_list = []

        while lefts:

            pop = lefts[0][0]
            temp = [elem[1] for elem in lefts if elem[0] == pop]
            grouped_list.append((pop, Op.Sigma(*temp)))
            lefts = [elem for elem in lefts if elem[0] != pop]

        function.Operands = [elem[0] * elem[1] for elem in grouped_list]


    elif function.Operator == Op.MUL:

        bases = []
        for elem in function.Operands:
            if elem.Operator == Op.POW:
                    bases.append((elem.Operands[0], elem.Operands[1]))
            else:
                bases.append((elem, ONE))


        grouped_list = []

        while bases:

            pop = bases[0][0]
            temp = [elem[1] for elem in bases if elem[0] == pop]
            grouped_list.append((pop, Op.Sigma(*temp)))
            bases = [elem for elem in bases if elem[0] != pop]
        #Here, I thought about b^x * c^x = (bc)^x, only true for b, c>= 0, Thus I wouldn't add this.
        function.Operands = [pow(elem[0], elem[1]) for elem in grouped_list]

    else:
        return function

#Isomorphism code.
'''
def Isomorphism():
    pass
'''































