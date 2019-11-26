# Principles

<br>

# Function

Since literally everything is function, the implementation of function class is almost equivalent to this project.

Function consists of parameters, operator, and operands. As I use tree structure for internal implementation, to describe
the body of a function, we separate it by operator and operands.

To define a function, there is two essentiatl subclasses of function which have priority over other functions. 

<br>

## ConstantMap

A constant function. Their declaration is straightforward. their value is literally equal to themselves.
```

ONE = ConstantMap(1)
ZERO = ConstantMap(0)
print(ZERO)
0
```
Throughout the procedure, the system immediately catches whether an expression is equivalent to some constant, and transforms it
into ConstantMap.

<br>

This is done by `IsConst()` which verifies whether a tree expression is actually a constant. One can give a reference parameter, so
that the tree expression is constant "with respect to specific set of variables".

```
Sin(False, PI * ConstantMap(3))
0
```
<br>

## IdentityMap

These is a class of function that becomes 'Parameter' of other function. In other words, variables like x, y, z, etc.
(Of course their parameter is themselves.)

In general sense of function, they are identity function `lambda x : x.` In lambda expression, 'x' can be replaced by any symbol. 
(Thus `lambda x : x` is equivalent `lambda y : y`.) 

However, when we talk about usage as parameter, we must specify what we are calling it. 
Thus in terms of Equality, not Equivalency,

```

VarX = IdentityMap('x') 
VarY = IdentityMap('y')
VarX == VarY
False

```
Hence IdentityMap is just a "Named identity lambda" 

<br>

## Operator

When we mean an operator, we generally think about `+`, `-`, `*`, `/`. However, in functional tree structure,
the concept is extended to some function operators and a differential operator 

```
Op.SIN, Op.COS Op.LN, Op.DEL 
```
and each operator object has an evaluation function for numerical calculation.

<br>

## UnitaryFunction

Unitary Function implies a function that is not separable by field operations. Thus, Unitary Functions have corresponding operators.
The below is built - in function Sin. The definition uses identitymap VarX.

```
Sin = Function((VarX,), Op.SIN, VarX)
```
<br>

## DefaultFunction

Users sometimes want to define own function that is self - defining. See an 'arbitrary' function f(x).

```
Fx = DefaultFunction( "f", (VarX,))
```

DefaultFunction() is not a class. It is a generator function with the name of it.

```
Fx.Operator
Op.DEFAULT
Fx.Operands
[x]
Fx.Name
'f'
```
Default functions have somewhat weird signature and processings, but that isn't important.

<br>

## Call Structure

Of course a function is callable. Usually call option is False, but someone can give a call option to declare a function 
like `f(x,y,z) = g(y,z,x)`
For example

```
DisgustingFunction = pow(VarX, VarX)
g = Sin(False, VarT) + DisgustingFunction(False, VarY)*VarW
g.Parameters
(t, y, w)
f = g((VarX, VarY, VarZ), VarY, VarZ, VarX)

print(f)
+( SIN(y), *(^(z, z), x) )

```
Field operation, such as addition, multiplication, subtraction, division and pow() is built - in operators that Function class
overrodes.

<br>

## Simplification Rule 

Our 'Philosophy of Simplification' is based on these statements.

<br>

**1. Minimize Syntactic Sugar.**

`-` and `/` are offered for convenience, but they become `+ *-1` and `* ^-1`. 

There is no `Op.LOG`. Instead, Log is implemented with `Ln/Ln` form.

Likewise, there is no `Op.TAN`. Tan is implemented with `Sin/Cos` form.

<br>

**2. Reduce The number of nodes in tree.**

`a^x * a^y` is `* (^(a, x), ^(a, y))` in tree expression, which can be reduced to `a^(x+y) = ^(a, +(x, y))`.

`ax + ay` is `+(*(a, x), *(a, y))` in tree expression, which can be reduced to `*(a, +(x, y))`

<br>

**3. Too many simplification is harmful - as Einstein said.**

Although `Ln(ab) = Ln(a) + Ln(b)` is included in our simplifier, `xLn(a)` does not change to `Ln(a^x)` since EXPONENT is 
cumbersome than product in many situations. Conversely, `Ln(e^x) = x, e^Ln(x) = x` are included.

(In general sense, Inverse Function Simplification is included.)

`b^x * c^x = (bc)^x` is valid for 2), but this holds only when terms are positive. Simplification should not lead to loss of 
information.

<br>

I will add specific simplifier setting later, but the algebra system offers default simplification setting. 
Basically there are 3 stages of simplification.

<br>

### Parser Stage

At this stage, the parser corrects redundant input, and effectively build tree in order to make further simplification easy.

```

((x+2)) = x+2
--4 = 4
3+ (x + yz ) = 3 + x + yz

```
<br>

### Operational Stage

When performing operation between functions, automatically some very important simplifications are done.

They consist of 3 stages:

<br>

**1) Remove redundant parenthesis**

**2) Order the operands, and preprocess constant terms**

**3) Group the operands (Distributive law, and exponenetial law)**

<br>

### Call Stage

Call is implemented (basically) by substitution, assuming the caller and callee are all simplified.

But after calling, it may be further simplificable. Thus we use CalculateTree() function to re - calculate the tree, invoking Operational Stages. (Top-Down Evalutation)

<br>

## Del 

`Function.Del` is a method taking one IdentityMap parameter. It is (partial) differentiation with respect to the given
IdentityMap parameter. 

General Differentiation Rules, Specific Derivatives and Simplifications are all implemented.

```

DisgustingFunction.Del(VarX)
*(x^x, +(1, LN(x))

```

<br>


## Isomorphism 


The product uses "Homomorphism Structure".

Since Function is a conceptual class, It is difficult to process operations on "specific" family of functions  
with only this conceptual class. 

"Homomorphism" is a function between two sets that preserves specific operation or characteristics. 
Here, they should be closed under the operation.

<br>

```
    f(a + b) = f(a) + f(b)
    f(ab) = f(a)f(b)
```

<br>

For example, this simple function above is Homomorphism on addition and multiplication.

If a homomorphism is injective, it's called monomorphism.

If a homomorphism is surjective, it's called ephimorphism.

If both, it's called Isomorphism. Our system is monomorphism - based. 

<br>

```
    Function class <----ConvertTo-------> Specific external class
    |                       (Clockwise)             |
    v                                               v
    Operations<--------ConvertTo-----------------> Operations

```

<br>

Diagram above fully describes how our system works. 

<br>

**1. Generate specific external instance and its pair - Function from ConvertTo() **

**2. Operation is called from Function class**

**3. Execute the paired operation from paired instance in the external class**

**4. Use ConvertTo() to obtain the result in Function class.**

<br>

To illustrate further, imagine Polynomial Multiplication - It is bothersome work 
within Tree structure. So is other polynomial - specific works and simplification.

```
    def __mul__(self, other):

        s, o = Pad_list(self.Coefficients, other.Degree, "L"), Pad_list(other.Coefficients, self.Degree, "L")
        s.reverse()
        o.reverse()

        # Cauchy Product.
        a = [sum([s[x] * o[k - x] for x in range(k+1)]) for k in range(self.Degree + other.Degree+1)]
        a.reverse()
        return Polynomial(a)

```
<br>


Thus we first process it within polynomial family, and convert back to Function class.
Since the two results should be identical Mathematically, we choose convenient order.

<br>

It is hard to 'generally' implement this structure with code 100%. Instead, I will be giving commands that specifies the family
of function, in order to apply the monomorphism. They will be:

```
Polynomials
Rational Functions
Trigonometric Series
Linear Transformations
Analytic Functions

And any other mathematical structures which have monomorphism structure.  
```


