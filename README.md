# SomethingLikeCAS
I love Algebra.


## Description

Analysis and Algebra system on real - valued single or multi variable functions. Primary goal of this project is
clearly to do Analysis and Algebra.^^

## Design Philosophy

Everything is a function.

Mathematical way is always best.

Isomorphisms are better than inheritance.

Parser should do 70% of simplification.

Equal things are equal.

Equivalent things are equal in some contexts.

The only we know is Identity map.

## Schedule 

난 내가 작업하고 싶을 때만 한다.

## Isomorphisms

The design principle of this project is "Homomorphism Structure".

class "Function" is merely conceptual class. This class provides essential
features of function objects ( Definition, Parameters, Calling, Tree structure )

However, it is difficult to process operations on "specific" family of functions  
with only this conceptual class. 

Therefore I formulated mathematical solution. "Homomorphism" is a function between
two sets that preserves specific operation or characteristics. Here, they should be 
closed under the operation.

```
    f(a + b) = f(a) + f(b)
    f(ab) = f(a)f(b)
```
For example, this simple function above is Homomorphism on addition and multiplication.

If a homomorphism is injective, it's called monomorphism.


If a homomorphism is surjective, it's called ephimorphism.

If both, it's called Isomorphism. Our system is monomorphism - based. 
```
    Function class <----ConvertTo-------> Specific external class
    |                (Counterclockwise)             |
    v                                               v
    Operations<--------ConvertTo-----------------> Operations

```
Diagram above fully describes how our system works. 
1. Generate specific external instance and its pair - Function from ConvertTo() 
2. Operation is called from Function class
3. Execute the paired operation from paired instance in the external class
4. Use ConvertTo() to obtain the result in Function class.

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
It is that easy in class "Polynomial".

Thus we first process it within polynomial family, and convert back to Function class.
Since the two results should be identical Mathematically, we choose convenient order.
that is our design principle.  