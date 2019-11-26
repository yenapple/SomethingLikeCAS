# Principles


# Function

Since literally everything is function, the implementation of function class is almost equivalent to this project.

Function consists of parameters, operator, and operands. As I use tree structure for internal implementation, to describe
the body of a function, we separate it by operator and operands.

To define a function, there is two essentiatl subclasses of function which have priority over other functions. 

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

```
Sin(False, PI * ConstantMap(3))
0
```

## IdentityMap

These is a class of function that becomes 'Parameter' of other function. In other words, variables like x, y, z, etc.
(Of course their parameter is themselves.)

In general sense of function, they are identity function 'lambda x : x.' In lambda expression, 'x' can be replaced by any symbol. 
(Thus lambda x : x is equivalent lambda y : y.) 

However, when we talk about usage as parameter, we must specify what we are calling it. 
Thus in terms of Equality, not Equivalency,

```

VarX = IdentityMap('x') 
VarY = IdentityMap('y')
VarX == VarY
False

```
Hence IdentityMap is just a "Named identity lambda" 


## Operator

When we mean an operator, we generally think about `+`, `-`, `*`, `/`. However, in functional tree structure,
the concept is extended to some function operators and a differential operator 

```
Op.SIN, Op.COS Op.LN, Op.DEL 
```


## UnitaryFunction

Unitary Function implies a function that is not separable by field operations. Thus, Unitary Functions have corresponding operators.
The below is built - in function Sin. The definition uses identitymap VarX.

```
Sin = Function((VarX,), Op.SIN, VarX)
```

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
Default functions have somewhat weird signature, but that isn't important.

## Call Structure

Of course a function is callable. Usually call option is False, but someone can give a call option to declare a function 
like f(x,y,z) = g(y,z,x)
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


