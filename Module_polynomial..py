import math
import functools

#Single variable polynomial processing class
class Polynomial:

    def __init__(self, coefficients):

        self.Coefficients = Trim_list(coefficients)
        self.Degree = len(self.Coefficients)-1

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