from __future__ import division

from sympy import (Add, Basic, S, Symbol, Wild,  Float, Integer, Rational, I,
    sin, cos, tan, exp, log, oo, sqrt, symbols, Integral, sympify, WildFunction,
    Poly, Function, Derivative, Number, pi, NumberSymbol, zoo, Piecewise, Mul,
    Pow, nsimplify, ratsimp, trigsimp, radsimp, powsimp, simplify, together,
    separate, collect, factorial, apart, combsimp, factor, refine, cancel,
    Tuple, default_sort_key, DiracDelta, gamma, Dummy, Sum)
from sympy.abc import a, b, c, d, e, n, t, u, x, y, z
from sympy.physics.secondquant import FockState

from sympy.utilities.pytest import raises, XFAIL

class DummyNumber(object):
    """
    Minimal implementation of a number that works with SymPy.

    If one has a Number class (e.g. Sage Integer, or some other custom class)
    that one wants to work well with SymPy, one has to implement at least the
    methods of this class DummyNumber, resp. its subclasses I5 and F1_1.

    Basically, one just needs to implement either __int__() or __float__() and
    then one needs to make sure that the class works with Python integers and
    with itself.
    """

    def __radd__(self, a):
        if isinstance(a, (int, float)):
            return a + self.number
        return NotImplemented

    def __truediv__(a, b):
        return a.__div__(b)

    def __rtruediv__(a, b):
        return a.__rdiv__(b)

    def __add__(self, a):
        if isinstance(a, (int, float, DummyNumber)):
            return self.number + a
        return NotImplemented

    def __rsub__(self, a):
        if isinstance(a, (int, float)):
            return a - self.number
        return NotImplemented

    def __sub__(self, a):
        if isinstance(a, (int, float, DummyNumber)):
            return self.number - a
        return NotImplemented

    def __rmul__(self, a):
        if isinstance(a, (int, float)):
            return a * self.number
        return NotImplemented

    def __mul__(self, a):
        if isinstance(a, (int, float, DummyNumber)):
            return self.number * a
        return NotImplemented

    def __rdiv__(self, a):
        if isinstance(a, (int, float)):
            return a / self.number
        return NotImplemented

    def __div__(self, a):
        if isinstance(a, (int, float, DummyNumber)):
            return self.number / a
        return NotImplemented

    def __rpow__(self, a):
        if isinstance(a, (int, float)):
            return a ** self.number
        return NotImplemented

    def __pow__(self, a):
        if isinstance(a, (int, float, DummyNumber)):
            return self.number ** a
        return NotImplemented

    def __pos__(self):
        return self.number

    def __neg__(self):
        return - self.number

class I5(DummyNumber):
    number = 5
    def __int__(self):
        return self.number

class F1_1(DummyNumber):
    number = 1.1
    def __float__(self):
        return self.number

i5 = I5()
f1_1 = F1_1()

# basic sympy objects
basic_objs = [
    Rational(2),
    Float("1.3"),
    x,
    y,
    pow(x,y)*y,
]

# all supported objects
all_objs = basic_objs + [
    5,
    5.5,
    i5,
    f1_1
]

def dotest(s):
    for x in all_objs:
        for y in all_objs:
            s(x,y)

def test_basic():
    def j(a,b):
        x = a
        x = +a
        x = -a
        x = a+b
        x = a-b
        x = a*b
        x = a/b
        x = a**b
    dotest(j)

def test_ibasic():
    def s(a,b):
        x = a
        x += b
        x = a
        x -= b
        x = a
        x *= b
        x = a
        x /= b
    dotest(s)

def test_relational():
    assert (pi < 3) == False
    assert (pi <= 3) == False
    assert (pi > 3) == True
    assert (pi >= 3) == True
    assert (-pi < 3) == True
    assert (-pi <= 3) == True
    assert (-pi > 3) == False
    assert (-pi >= 3) == False
    assert (x - 2 < x - 3) == False

def test_relational_noncommutative():
    from sympy import Lt, Gt, Le, Ge
    A, B = symbols('A,B', commutative=False)
    assert (A < B)  == Lt(A, B)
    assert (A <= B) == Le(A, B)
    assert (A > B)  == Gt(A, B)
    assert (A >= B) == Ge(A, B)

def test_basic_nostr():
    for obj in basic_objs:
        for op in ['+','-','*','/','**']:
            if obj == 2 and op == '*':
                if hasattr(int, '__index__'): # Python 2.5+ (PEP 357)
                    assert obj * '1' == '11'
            else:
                raises(TypeError, "obj %s '1'" % op)

def test_leadterm():
    assert (3+2*x**(log(3)/log(2)-1)).leadterm(x) == (3,0)

    assert (1/x**2+1+x+x**2).leadterm(x)[1] == -2
    assert (1/x+1+x+x**2).leadterm(x)[1] == -1
    assert (x**2+1/x).leadterm(x)[1] == -1
    assert (1+x**2).leadterm(x)[1] == 0
    assert (x+1).leadterm(x)[1] == 0
    assert (x+x**2).leadterm(x)[1] == 1
    assert (x**2).leadterm(x)[1] == 2

def test_as_leading_term():
    assert (3+2*x**(log(3)/log(2)-1)).as_leading_term(x) == 3
    assert (1/x**2+1+x+x**2).as_leading_term(x) == 1/x**2
    assert (1/x+1+x+x**2).as_leading_term(x) == 1/x
    assert (x**2+1/x).as_leading_term(x) == 1/x
    assert (1+x**2).as_leading_term(x) == 1
    assert (x+1).as_leading_term(x) == 1
    assert (x+x**2).as_leading_term(x) == x
    assert (x**2).as_leading_term(x) == x**2

def test_leadterm2():
    assert (x*cos(1)*cos(1 + sin(1)) + sin(1 + sin(1))).leadterm(x) == \
            (sin(1 + sin(1)), 0)

def test_leadterm3():
    assert (y+z+x).leadterm(x) == (y+z, 0)

def test_as_leading_term2():
    assert (x*cos(1)*cos(1 + sin(1)) + sin(1 + sin(1))).as_leading_term(x) == \
            sin(1 + sin(1))

def test_as_leading_term3():
    assert (2+pi+x).as_leading_term(x) == 2 + pi
    assert (2*x+pi*x+x**2).as_leading_term(x) == (2+pi)*x

def test_atoms():
    assert sorted(list(x.atoms())) == [x]
    assert sorted(list((1+x).atoms())) == sorted([1, x])

    assert sorted(list((1+2*cos(x)).atoms(Symbol))) == [x]
    assert sorted(list((1+2*cos(x)).atoms(Symbol,Number))) == sorted([1, 2, x])

    assert sorted(list((2*(x**(y**x))).atoms())) == sorted([2, x, y])

    assert sorted(list(Rational(1,2).atoms())) == [S.Half]
    assert sorted(list(Rational(1,2).atoms(Symbol))) == []

    assert sorted(list(sin(oo).atoms(oo))) == [oo]

    assert sorted(list(Poly(0, x).atoms())) == [S.Zero]
    assert sorted(list(Poly(1, x).atoms())) == [S.One]

    assert sorted(list(Poly(x, x).atoms())) == [x]
    assert sorted(list(Poly(x, x, y).atoms())) == [x]
    assert sorted(list(Poly(x + y, x, y).atoms())) == sorted([x, y])
    assert sorted(list(Poly(x + y, x, y, z).atoms())) == sorted([x, y])
    assert sorted(list(Poly(x + y*t, x, y, z).atoms())) == sorted([t, x, y])

    assert list((I*pi).atoms(NumberSymbol)) == [pi]
    assert sorted((I*pi).atoms(NumberSymbol, I)) == \
           sorted((I*pi).atoms(I,NumberSymbol)) == [pi, I]


    assert exp(exp(x)).atoms(exp) == set([exp(exp(x)), exp(x)])
    assert (1 + x*(2 + y)+exp(3 + z)).atoms(Add) == set(
                                                   [1 + x*(2 + y)+exp(3 + z),
                                                    2 + y,
                                                    3 + z])

def test_is_polynomial():
    k = Symbol('k', nonnegative=True, integer=True)

    assert Rational(2).is_polynomial(x, y, z) == True
    assert (S.Pi).is_polynomial(x, y, z) == True

    assert x.is_polynomial(x) == True
    assert x.is_polynomial(y) == True

    assert (x**2).is_polynomial(x) == True
    assert (x**2).is_polynomial(y) == True

    assert (x**(-2)).is_polynomial(x) == False
    assert (x**(-2)).is_polynomial(y) == True

    assert (2**x).is_polynomial(x) == False
    assert (2**x).is_polynomial(y) == True

    assert (x**k).is_polynomial(x) == False
    assert (x**k).is_polynomial(k) == False
    assert (x**x).is_polynomial(x) == False
    assert (k**k).is_polynomial(k) == False
    assert (k**x).is_polynomial(k) == False

    assert (x**(-k)).is_polynomial(x) == False
    assert ((2*x)**k).is_polynomial(x) == False

    assert (x**2 + 3*x - 8).is_polynomial(x) == True
    assert (x**2 + 3*x - 8).is_polynomial(y) == True

    assert (x**2 + 3*x - 8).is_polynomial() == True

    assert sqrt(x).is_polynomial(x) == False
    assert (sqrt(x)**3).is_polynomial(x) == False

    assert (x**2 + 3*x*sqrt(y) - 8).is_polynomial(x) == True
    assert (x**2 + 3*x*sqrt(y) - 8).is_polynomial(y) == False

    assert ((x**2)*(y**2) + x*(y**2) + y*x + exp(2)).is_polynomial() == True
    assert ((x**2)*(y**2) + x*(y**2) + y*x + exp(x)).is_polynomial() == False

    assert ((x**2)*(y**2) + x*(y**2) + y*x + exp(2)).is_polynomial(x, y) == True
    assert ((x**2)*(y**2) + x*(y**2) + y*x + exp(x)).is_polynomial(x, y) == False

def test_is_rational_function():
    assert Integer(1).is_rational_function() == True
    assert Integer(1).is_rational_function(x) == True

    assert Rational(17,54).is_rational_function() == True
    assert Rational(17,54).is_rational_function(x) == True

    assert (12/x).is_rational_function() == True
    assert (12/x).is_rational_function(x) == True

    assert (x/y).is_rational_function() == True
    assert (x/y).is_rational_function(x) == True
    assert (x/y).is_rational_function(x, y) == True

    assert (x**2+1/x/y).is_rational_function() == True
    assert (x**2+1/x/y).is_rational_function(x) == True
    assert (x**2+1/x/y).is_rational_function(x, y) == True

    assert (sin(y)/x).is_rational_function() == False
    assert (sin(y)/x).is_rational_function(y) == False
    assert (sin(y)/x).is_rational_function(x) == True
    assert (sin(y)/x).is_rational_function(x, y) == False

def test_SAGE1():
    #see http://code.google.com/p/sympy/issues/detail?id=247
    class MyInt:
        def _sympy_(self):
            return Integer(5)
    m = MyInt()
    e = Rational(2)*m
    assert e == 10

    raises(TypeError, "Rational(2)*MyInt")

def test_SAGE2():
    class MyInt(object):
        def __int__(self):
            return 5
    assert sympify(MyInt()) == 5
    e = Rational(2)*MyInt()
    assert e == 10

    raises(TypeError, "Rational(2)*MyInt")

def test_SAGE3():
    class MySymbol:
        def __rmul__(self, other):
            return ('mys', other, self)

    o = MySymbol()
    e = x*o

    assert e == ('mys', x, o)

def test_len():
    e = x*y
    assert len(e.args) == 2
    e = x+y+z
    assert len(e.args) == 3

def test_doit():
    a = Integral(x**2, x)

    assert isinstance(a.doit(), Integral) == False

    assert isinstance(a.doit(integrals=True), Integral) == False
    assert isinstance(a.doit(integrals=False), Integral) == True

    assert (2*Integral(x, x)).doit() == x**2

def test_attribute_error():
    raises(AttributeError, "x.cos()")
    raises(AttributeError, "x.sin()")
    raises(AttributeError, "x.exp()")

def test_args():
    assert (x*y).args in ((x, y), (y, x))
    assert (x+y).args in ((x, y), (y, x))
    assert (x*y+1).args in ((x*y, 1), (1, x*y))
    assert sin(x*y).args == (x*y,)
    assert sin(x*y).args[0] == x*y
    assert (x**y).args == (x,y)
    assert (x**y).args[0] == x
    assert (x**y).args[1] == y

def test_iter_basic_args():
    assert list(sin(x*y).iter_basic_args()) == [x*y]
    assert list((x**y).iter_basic_args()) == [x, y]

def test_noncommutative_expand_issue658():
    A, B, C = symbols('A,B,C', commutative=False)
    assert A*B - B*A != 0
    assert (A*(A+B)*B).expand() == A**2*B + A*B**2
    assert (A*(A+B+C)*B).expand() == A**2*B + A*B**2 + A*C*B

def test_as_numer_denom():
    assert oo.as_numer_denom() == (1, 0)
    assert (-oo).as_numer_denom() == (-1, 0)
    assert zoo.as_numer_denom() == (zoo, 1)
    assert (-zoo).as_numer_denom() == (zoo, 1)

    assert x.as_numer_denom() == (x, 1)
    assert (1/x).as_numer_denom() == (1, x)
    assert (x/y).as_numer_denom() == (x, y)
    assert (x/2).as_numer_denom() == (x, 2)
    assert (x*y/z).as_numer_denom() == (x*y, z)
    assert (x/(y*z)).as_numer_denom() == (x, y*z)
    assert Rational(1, 2).as_numer_denom() == (1, 2)
    assert (1/y**2).as_numer_denom() == (1, y**2)
    assert (x/y**2).as_numer_denom() == (x, y**2)
    assert ((x**2+1)/y).as_numer_denom() == (x**2+1, y)
    assert (x*(y+1)/y**7).as_numer_denom() == (x*(y+1), y**7)
    assert (x**-2).as_numer_denom() == (1, x**2)
    n = symbols('n', negative=True)
    assert (x**n).as_numer_denom() == (x**n, 1)
    assert sqrt(1/n).as_numer_denom() == (I, sqrt(-n))
    n = Symbol('0 or neg', nonpositive=True)
    assert (1/sqrt(x/n)).as_numer_denom() == (1, sqrt(x/n))
    assert (a/x + b/2/x + c/3/x).as_numer_denom() == \
            (6*a + 3*b + 2*c, 6*x)
    assert (a/x + b/2/x + c/3/y).as_numer_denom() == \
            (2*c*x + y*(6*a + 3*b), 6*x*y)
    assert (a/x + b/2/x + c/.5/x).as_numer_denom() == \
            (2*a + b + 4.0*c, 2*x)
    # this should take no more than a few seconds
    assert int(log(Add(*[Dummy()/i/x for i in xrange(1, 705)]
                       ).as_numer_denom()[1]/x).n(4)) == 705
    for i in [S.Infinity, S.NegativeInfinity, S.ComplexInfinity]:
        assert (i + x/3).as_numer_denom() == \
            (x + i, 3)
    assert (S.Infinity + x/3 + y/4).as_numer_denom() == \
        (4*x + 3*y + S.Infinity, 12)
    assert (oo*x + zoo*y).as_numer_denom() == \
        (zoo*y + oo*x, 1)

    A, B, C = symbols('A,B,C', commutative=False)

    assert (A*B*C**-1).as_numer_denom() == (A*B*C**-1, 1)
    assert (A*B*C**-1/x).as_numer_denom() == (A*B*C**-1, x)
    assert (C**-1*A*B).as_numer_denom() == (C**-1*A*B, 1)
    assert (C**-1*A*B/x).as_numer_denom() == (C**-1*A*B, x)
    assert ((A*B*C)**-1).as_numer_denom() == ((A*B*C)**-1, 1)
    assert ((A*B*C)**-1/x).as_numer_denom() == ((A*B*C)**-1, x)

def test_as_independent():
    assert (2*x*sin(x)+y+x).as_independent(x) == (y, x + 2*x*sin(x))
    assert (2*x*sin(x)+y+x).as_independent(y) == (x + 2*x*sin(x), y)

    assert (2*x*sin(x)+y+x).as_independent(x, y) == (0, y + x + 2*x*sin(x))

    assert (x*sin(x)*cos(y)).as_independent(x) == (cos(y), x*sin(x))
    assert (x*sin(x)*cos(y)).as_independent(y) == (x*sin(x), cos(y))

    assert (x*sin(x)*cos(y)).as_independent(x, y) == (1, x*sin(x)*cos(y))

    assert (sin(x)).as_independent(x) == (1, sin(x))
    assert (sin(x)).as_independent(y) == (sin(x), 1)

    assert (2*sin(x)).as_independent(x) == (2, sin(x))
    assert (2*sin(x)).as_independent(y) == (2*sin(x), 1)

    # issue 1804 = 1766b
    n1, n2, n3 = symbols('n1 n2 n3', commutative=False)
    assert (n1 + n1*n2).as_independent(n2) == (n1, n1*n2)
    assert (n2*n1 + n1*n2).as_independent(n2) == (0, n1*n2 + n2*n1)
    assert (n1*n2*n1).as_independent(n2) == (n1, n2*n1)
    assert (n1*n2*n1).as_independent(n1) == (1, n1*n2*n1)

    assert (3*x).as_independent(x, as_Add=True) == (0, 3*x)
    assert (3*x).as_independent(x, as_Add=False) == (3, x)
    assert (3+x).as_independent(x, as_Add=True) == (3, x)
    assert (3+x).as_independent(x, as_Add=False) == (1, 3 + x)

    # issue 2380
    assert (3*x).as_independent(Symbol) == (3, x)

    # issue 2549
    assert (n1*x*y).as_independent(x) == (n1*y, x)
    assert ((x + n1)*(x - y)).as_independent(x) == (1, (x + n1)*(x - y))
    assert ((x + n1)*(x - y)).as_independent(y) == (x + n1, x - y)
    assert (DiracDelta(x - n1)*DiracDelta(x - y)).as_independent(x) == (1, DiracDelta(x - n1)*DiracDelta(x - y))
    assert (x*y*n1*n2*n3).as_independent(n2) == (x*y*n1, n2*n3)
    assert (x*y*n1*n2*n3).as_independent(n1) == (x*y, n1*n2*n3)
    assert (x*y*n1*n2*n3).as_independent(n3) == (x*y*n1*n2, n3)
    assert (DiracDelta(x - n1)*DiracDelta(y - n1)*DiracDelta(x - n2)).as_independent(y) == \
           (DiracDelta(x - n1), DiracDelta(y - n1)*DiracDelta(x - n2))

    # issue 2685
    assert (x + Integral(x, (x, 1, 2))).as_independent(x, strict=True) == \
           (Integral(x, (x, 1, 2)), x)

def test_subs_dict():
    assert (sin(x))._subs_dict({ x : 1, sin(x) : 2}) == 2
    assert (sin(x))._subs_dict([(x, 1), (sin(x), 2)]) == 2

    expr = sqrt(sin(2*x))*sin(exp(x)*x)*cos(2*x) + sin(2*x)

    seq = [ (sqrt(sin(2*x)),a), (cos(2*x),b), (sin(2*x),c), (x,d), (exp(x),e) ]
    assert expr._subs_dict(seq) == c + a*b*sin(d*e)

    seq = [ (sqrt(sin(2*x)),a), (sin(2*x),c), (cos(2*x),b), (x,d), (exp(x),e) ]
    assert expr._subs_dict(seq) == c + a*b*sin(d*e)

def test_subs_list():
    assert (sin(x))._subs_list([(sin(x), 2), (x, 1)]) == 2
    assert (sin(x))._subs_list([(x, 1), (sin(x), 2)]) == sin(1)

    assert (x+y)._subs_list([(x, 3), (y, x**2)]) == 3 + x**2
    assert (x+y)._subs_list([(y, x**2), (x, 3)]) == 12

def test_call():
    # Unlike what used to be the case, the following should NOT work.
    # See issue 1927.

    raises(TypeError, "sin(x)({ x : 1, sin(x) : 2})")
    raises(TypeError, "sin(x)(1)")

def test_replace():
    f = log(sin(x)) + tan(sin(x**2))

    assert f.replace(sin, cos) == log(cos(x)) + tan(cos(x**2))
    assert f.replace(sin, lambda a: sin(2*a)) == log(sin(2*x)) + tan(sin(2*x**2))

    a = Wild('a')

    assert f.replace(sin(a), cos(a)) == log(cos(x)) + tan(cos(x**2))
    assert f.replace(sin(a), lambda a: sin(2*a)) == log(sin(2*x)) + tan(sin(2*x**2))

    g = 2*sin(x**3)

    assert g.replace(lambda expr: expr.is_Number, lambda expr: expr**2) == 4*sin(x**9)

    assert cos(x).replace(cos, sin, map=True) == (sin(x), {cos(x): sin(x)})
    assert sin(x).replace(cos, sin) == sin(x)

    assert (y*sin(x)).replace(sin, lambda expr: sin(expr)/y) == sin(x)

def test_find():
    expr = (x + y + 2 + sin(3*x))

    assert expr.find(lambda u: u.is_Integer) == set([S(2), S(3)])
    assert expr.find(lambda u: u.is_Symbol) == set([x, y])

    assert expr.find(lambda u: u.is_Integer, group=True) == {S(2): 1, S(3): 1}
    assert expr.find(lambda u: u.is_Symbol, group=True) == {x: 2, y: 1}

    assert expr.find(Integer) == set([S(2), S(3)])
    assert expr.find(Symbol) == set([x, y])

    assert expr.find(Integer, group=True) == {S(2): 1, S(3): 1}
    assert expr.find(Symbol, group=True) == {x: 2, y: 1}

    a = Wild('a')

    expr = sin(sin(x)) + sin(x) + cos(x) + x

    assert expr.find(lambda u: type(u) is sin) == set([sin(x), sin(sin(x))])
    assert expr.find(lambda u: type(u) is sin, group=True) == {sin(x): 2, sin(sin(x)): 1}

    assert expr.find(sin(a)) == set([sin(x), sin(sin(x))])
    assert expr.find(sin(a), group=True) == {sin(x): 2, sin(sin(x)): 1}

    assert expr.find(sin) == set([sin(x), sin(sin(x))])
    assert expr.find(sin, group=True) == {sin(x): 2, sin(sin(x)): 1}

def test_count():
    expr = (x + y + 2 + sin(3*x))

    assert expr.count(lambda u: u.is_Integer) == 2
    assert expr.count(lambda u: u.is_Symbol) == 3

    assert expr.count(Integer) == 2
    assert expr.count(Symbol) == 3
    assert expr.count(2) == 1

    a = Wild('a')

    assert expr.count(sin) == 1
    assert expr.count(sin(a)) == 1
    assert expr.count(lambda u: type(u) is sin) == 1

def test_has_basics():
    f = Function('f')
    g = Function('g')
    p = Wild('p')

    assert sin(x).has(x)
    assert sin(x).has(sin)
    assert not sin(x).has(y)
    assert not sin(x).has(cos)
    assert f(x).has(x)
    assert f(x).has(f)
    assert not f(x).has(y)
    assert not f(x).has(g)

    assert f(x).diff(x).has(x)
    assert f(x).diff(x).has(f)
    assert f(x).diff(x).has(Derivative)
    assert not f(x).diff(x).has(y)
    assert not f(x).diff(x).has(g)
    assert not f(x).diff(x).has(sin)

    assert (x**2).has(Symbol)
    assert not (x**2).has(Wild)
    assert (2*p).has(Wild)

    assert not x.has()

def test_has_multiple():
    f = x**2*y + sin(2**t + log(z))

    assert f.has(x)
    assert f.has(y)
    assert f.has(z)
    assert f.has(t)

    assert not f.has(u)

    assert f.has(x, y, z, t)
    assert f.has(x, y, z, t, u)

    i = Integer(4400)

    assert not i.has(x)

    assert (i*x**i).has(x)
    assert not (i*y**i).has(x)
    assert (i*y**i).has(x, y)
    assert not (i*y**i).has(x, z)

def test_has_piecewise():
    f = (x*y + 3/y)**(3 + 2)
    g = Function('g')
    h = Function('h')
    p = Piecewise((g, x < -1), (1, x <= 1), (f, True))

    assert p.has(x)
    assert p.has(y)
    assert not p.has(z)
    assert p.has(1)
    assert p.has(3)
    assert not p.has(4)
    assert p.has(f)
    assert p.has(g)
    assert not p.has(h)

def test_has_iterative():
    A, B, C = symbols('A,B,C', commutative=False)
    f = x*gamma(x)*sin(x)*exp(x*y)*A*B*C*cos(x*A*B)

    assert f.has(x)
    assert f.has(x*y)
    assert f.has(x*sin(x))
    assert not f.has(x*sin(y))
    assert f.has(x*A)
    assert f.has(x*A*B)
    assert not f.has(x*A*C)
    assert f.has(x*A*B*C)
    assert not f.has(x*A*C*B)
    assert f.has(x*sin(x)*A*B*C)
    assert not f.has(x*sin(x)*A*C*B)
    assert not f.has(x*sin(y)*A*B*C)
    assert f.has(x*gamma(x))

def test_has_integrals():
    f = Integral(x**2 + sin(x*y*z), (x, 0, x + y + z))

    assert f.has(x + y)
    assert f.has(x + z)
    assert f.has(y + z)

    assert f.has(x*y)
    assert f.has(x*z)
    assert f.has(y*z)

    assert not f.has(2*x + y)
    assert not f.has(2*x*y)

def test_has_tuple():
    f = Function('f')
    g = Function('g')
    h = Function('h')

    assert Tuple(x, y).has(x)
    assert not Tuple(x, y).has(z)
    assert Tuple(f(x), g(x)).has(x)
    assert not Tuple(f(x), g(x)).has(y)
    assert Tuple(f(x), g(x)).has(f)
    assert Tuple(f(x), g(x)).has(f(x))
    assert not Tuple(f, g).has(x)
    assert Tuple(f, g).has(f)
    assert not Tuple(f, g).has(h)

def test_has_units():
    from sympy.physics.units import m, s

    assert (x*m/s).has(x)
    assert (x*m/s).has(y, z) is False

def test_has_polys():
    poly = Poly(x**2 + x*y*sin(z), x, y, t)

    assert poly.has(x)
    assert poly.has(x, y, z)
    assert poly.has(x, y, z, t)

def test_has_physics():
    assert FockState((x, y)).has(x)

def test_as_poly_as_expr():
    f = x**2 + 2*x*y

    assert f.as_poly().as_expr() == f
    assert f.as_poly(x, y).as_expr() == f

    assert (f + sin(x)).as_poly(x, y) is None

    p = Poly(f, x, y)

    assert p.as_poly() == p

def test_nonzero():
    assert bool(S.Zero) == False
    assert bool(S.One)  == True
    assert bool(x)      == True
    assert bool(x+y)    == True
    assert bool(x-x)    == False
    assert bool(x*y)    == True
    assert bool(x*1)    == True
    assert bool(x*0)    == False

def test_is_number():
    assert Float(3.14).is_number == True
    assert Integer(737).is_number == True
    assert Rational(3, 2).is_number == True
    assert Rational(8).is_number == True
    assert x.is_number == False
    assert (2*x).is_number == False
    assert (x + y).is_number == False
    assert log(2).is_number == True
    assert log(x).is_number == False
    assert (2 + log(2)).is_number == True
    assert (8+log(2)).is_number == True
    assert (2 + log(x)).is_number == False
    assert (8+log(2)+x).is_number == False
    assert (1+x**2/x-x).is_number == True
    assert Tuple(Integer(1)).is_number == False
    assert Add(2, x).is_number == False
    assert Mul(3, 4).is_number == True
    assert Pow(log(2), 2).is_number == True
    assert oo.is_number == True
    g = WildFunction('g')
    assert g.is_number == False
    assert (2*g).is_number == False
    assert (x**2).subs(x, 3).is_number == True

    # test extensibility of .is_number
    # on subinstances of Basic
    class A(Basic):
        pass
    a = A()
    assert a.is_number == False

def test_as_coeff_add():
    assert S(2).as_coeff_add() == (2, ())
    assert S(3.0).as_coeff_add() == (0, (S(3.0),))
    assert S(-3.0).as_coeff_add() == (0, (S(-3.0),))
    assert     x .as_coeff_add() == ( 0, (x,))
    assert (-1+x).as_coeff_add() == (-1, (x,))
    assert ( 2+x).as_coeff_add() == ( 2, (x,))
    assert ( 1+x).as_coeff_add() == ( 1, (x,))
    assert (x + y).as_coeff_add(y) == (x, (y,))
    assert (3*x).as_coeff_add(y) == (3*x, ())
    # don't do expansion
    e = (x + y)**2
    assert e.as_coeff_add(y) == (0, (e,))

def test_as_coeff_mul():
    assert S(2).as_coeff_mul() == (2, ())
    assert S(3.0).as_coeff_mul() == (1, (S(3.0),))
    assert S(-3.0).as_coeff_mul() == (-1, (S(3.0),))
    assert     x .as_coeff_mul() == ( 1, (x,))
    assert (-x).as_coeff_mul() == (-1, (x,))
    assert (2*x).as_coeff_mul() == (2, (x,))
    assert (x*y).as_coeff_mul(y) == (x, (y,))
    assert (3 + x).as_coeff_mul(y) == (3 + x, ())
    # don't do expansion
    e = exp(x + y)
    assert e.as_coeff_mul(y) == (1, (e,))
    e = 2**(x + y)
    assert e.as_coeff_mul(y) == (1, (e,))

def test_as_coeff_exponent():
    assert (3*x**4).as_coeff_exponent(x) == (3, 4)
    assert (2*x**3).as_coeff_exponent(x) == (2, 3)
    assert (4*x**2).as_coeff_exponent(x) == (4, 2)
    assert (6*x**1).as_coeff_exponent(x) == (6, 1)
    assert (3*x**0).as_coeff_exponent(x) == (3, 0)
    assert (2*x**0).as_coeff_exponent(x) == (2, 0)
    assert (1*x**0).as_coeff_exponent(x) == (1, 0)
    assert (0*x**0).as_coeff_exponent(x) == (0, 0)
    assert (-1*x**0).as_coeff_exponent(x) == (-1, 0)
    assert (-2*x**0).as_coeff_exponent(x) == (-2, 0)
    assert (2*x**3+pi*x**3).as_coeff_exponent(x) == (2+pi, 3)
    assert (x*log(2)/(2*x + pi*x)).as_coeff_exponent(x) == \
            (log(2)/(2+pi), 0)
    # 1685
    D = Derivative
    f = Function('f')
    fx  = D(f(x), x)
    assert fx.as_coeff_exponent(f(x)) == (fx ,0)

def test_extractions():
    n = Symbol("n", integer=True)
    assert ((x*y)**3).extract_multiplicatively(x**2 * y) == x*y**2
    assert ((x*y)**3).extract_multiplicatively(x**4 * y) == None
    assert (2*x).extract_multiplicatively(2) == x
    assert (2*x).extract_multiplicatively(3) == None
    assert (2*x).extract_multiplicatively(-1) == None
    assert (Rational(1,2)*x).extract_multiplicatively(3) == x/6
    assert (sqrt(x)).extract_multiplicatively(x) == None
    assert (sqrt(x)).extract_multiplicatively(1/x) == sqrt(x)**3

    assert ((x*y)**3).extract_additively(1) == None
    assert (x+1).extract_additively(x) == 1
    assert (x+1).extract_additively(2*x) == None
    assert (x+1).extract_additively(-x) == 1+2*x
    assert (-x+1).extract_additively(2*x) == 1-3*x

    assert (Integer(-3)).could_extract_minus_sign() == True
    assert (-n*x+x).could_extract_minus_sign() != (n*x-x).could_extract_minus_sign()
    assert (x-y).could_extract_minus_sign() != (-x+y).could_extract_minus_sign()
    assert (1-x-y).could_extract_minus_sign() == True
    assert (1-x+y).could_extract_minus_sign() == False
    assert ((-x-x*y)/y).could_extract_minus_sign() == True
    assert (-(x+x*y)/y).could_extract_minus_sign() ==  True
    assert ((x+x*y)/(-y)).could_extract_minus_sign() == True
    assert ((x+x*y)/y).could_extract_minus_sign() == False
    assert (x*(-x-x**3)).could_extract_minus_sign() == True # used to give inf recurs
    assert ((-x-y)/(x+y)).could_extract_minus_sign() == True # is_Mul odd case
    # The results of each of these will vary on different machines, e.g.
    # the first one might be False and the other (then) is true or vice versa,
    # so both are included.
    assert ((-x-y)/(x-y)).could_extract_minus_sign() == False or\
           ((-x-y)/(y-x)).could_extract_minus_sign() == False # is_Mul even case
    assert ( x - y).could_extract_minus_sign() == False
    assert (-x + y).could_extract_minus_sign() == True

def test_coeff():
    assert (x+1).coeff(x+1) == 1
    assert (3*x).coeff(0) == None
    assert (z*(1+x)*x**2).coeff(1+x) == z*x**2
    assert (1+2*x*x**(1+x)).coeff(x*x**(1+x)) == 2
    assert (1+2*x**(y+z)).coeff(x**(y+z)) == 2
    assert (3+2*x+4*x**2).coeff(1) == None
    assert (3+2*x+4*x**2).coeff(-1) == None
    assert (3+2*x+4*x**2).coeff(x) == 2
    assert (3+2*x+4*x**2).coeff(x**2) == 4
    assert (3+2*x+4*x**2).coeff(x**3) == None

    assert (-x/8 + x*y).coeff(x) == -S(1)/8 + y
    assert (-x/8 + x*y).coeff(-x) == S(1)/8
    assert (4*x).coeff(2*x) == None
    assert (2*x).coeff(2*x) == 1

    n1, n2 = symbols('n1 n2', commutative=False)
    assert (n1*n2).coeff(n1) == 1
    assert (n1*n2).coeff(n2) == n1
    assert (n1*n2 + x*n1).coeff(n1) == 1 # 1*n1*(n2+x)
    assert (n2*n1 + x*n1).coeff(n1) == n2 + x
    assert (n2*n1 + x*n1**2).coeff(n1) == n2
    assert (n1**x).coeff(n1) == None
    assert (n1*n2 + n2*n1).coeff(n1) == None
    assert (2*(n1+n2)*n2).coeff(n1+n2, right=1) == n2
    assert (2*(n1+n2)*n2).coeff(n1+n2, right=0) == 2

    f = Function('f')
    assert (2*f(x) + 3*f(x).diff(x)).coeff(f(x)) == 2

    expr = z*(x+y)**2
    expr2 = z*(x+y)**2 + z*(2*x + 2*y)**2
    assert expr.coeff(z) == (x+y)**2
    assert expr.coeff(x+y) == None
    assert expr2.coeff(z) == (x+y)**2 + (2*x + 2*y)**2

    assert (x + y + 3*z).coeff(1) == x + y
    assert (-x + 2*y).coeff(-1) == x
    assert (x - 2*y).coeff(-1) == 2*y
    assert (3 + 2*x + 4*x**2).coeff(1) == None
    assert (-x - 2*y).coeff(2) == -y
    assert (x + sqrt(2)*x).coeff(sqrt(2)) == x
    assert (3 + 2*x + 4*x**2).coeff(x) ==  2
    assert (3 + 2*x + 4*x**2).coeff(x**2) == 4
    assert (3 + 2*x + 4*x**2).coeff(x**3) == None
    assert (z*(x + y)**2).coeff((x+y)**2) == z
    assert (z*(x + y)**2).coeff(x+y) == None
    assert (2 + 2*x + (x+1)*y).coeff(x+1) == y

    n, m, o, l = symbols('n m o l', commutative=False)
    assert n.coeff(n) ==  1
    assert y.coeff(n) == None
    assert (3*n).coeff(n) == 3
    assert (2 + n).coeff(x*m) == None
    assert (2*x*n*m).coeff(x) == 2*n*m
    assert (2 + n).coeff(x*m*n + y) == None
    assert (2*x*n*m).coeff(3*n) == None
    assert (n*m + m*n*m).coeff(n) == 1 + m
    assert (n*m + m*n*m).coeff(n, right=True) == m # = (1 + m)*n*m
    assert (n*m + m*n).coeff(n) == None
    assert (n*m + o*m*n).coeff(m*n) == o
    assert (n*m + o*m*n).coeff(m*n, right=1) == 1
    assert (n*m + n*m*n).coeff(n*m, right=1) == 1 + n # = n*m*(n + 1)

def test_coeff2():
    r, kappa = symbols('r, kappa')
    psi = Function("psi")
    g = 1/r**2 * (2*r*psi(r).diff(r, 1) + r**2 * psi(r).diff(r, 2))
    g = g.expand()
    assert g.coeff((psi(r).diff(r))) == 2/r

def test_coeff2_0():
    r, kappa = symbols('r, kappa')
    psi = Function("psi")
    g = 1/r**2 * (2*r*psi(r).diff(r, 1) + r**2 * psi(r).diff(r, 2))
    g = g.expand()

    assert g.coeff(psi(r).diff(r, 2)) == 1

def test_coeff_expand():
    expr = z*(x+y)**2
    expr2 = z*(x+y)**2 + z*(2*x + 2*y)**2
    assert expr.coeff(z) == (x+y)**2
    assert expr2.coeff(z) == (x+y)**2 + (2*x + 2*y)**2

def test_integrate():
    assert x.integrate(x) == x**2/2
    assert x.integrate((x, 0, 1)) == S(1)/2

def test_as_base_exp():
    assert x.as_base_exp() == (x, S.One)
    assert (x*y*z).as_base_exp() == (x*y*z, S.One)
    assert (x+y+z).as_base_exp() == (x+y+z, S.One)
    assert ((x+y)**z).as_base_exp() == (x+y, z)

def test_issue1864():
    assert hasattr(Mul(x, y), "is_commutative")
    assert hasattr(Mul(x, y, evaluate=False), "is_commutative")
    assert hasattr(Pow(x, y), "is_commutative")
    assert hasattr(Pow(x, y, evaluate=False), "is_commutative")
    expr = Mul(Pow(2, 2, evaluate=False), 3, evaluate=False) + 1
    assert hasattr(expr, "is_commutative")

def test_action_verbs():
    assert nsimplify((1/(exp(3*pi*x/5)+1))) == (1/(exp(3*pi*x/5)+1)).nsimplify()
    assert ratsimp(1/x + 1/y) == (1/x + 1/y).ratsimp()
    assert trigsimp(log(x), deep=True) == (log(x)).trigsimp(deep = True)
    assert radsimp(1/(2+sqrt(2))) == (1/(2+sqrt(2))).radsimp()
    assert powsimp(x**y*x**z*y**z, combine='all') == (x**y*x**z*y**z).powsimp(combine='all')
    assert simplify(x**y*x**z*y**z) == (x**y*x**z*y**z).simplify()
    assert together(1/x + 1/y) == (1/x + 1/y).together()
    assert separate((x*(y*z)**3)**2) == ((x*(y*z)**3)**2).separate()
    assert collect(a*x**2 + b*x**2 + a*x - b*x + c, x) == (a*x**2 + b*x**2 + a*x - b*x + c).collect(x)
    assert apart(y/(y+2)/(y+1), y) == (y/(y+2)/(y+1)).apart(y)
    assert combsimp(y/(x+2)/(x+1)) == (y/(x+2)/(x+1)).combsimp()
    assert factor(x**2+5*x+6) == (x**2+5*x+6).factor()
    assert refine(sqrt(x**2)) == sqrt(x**2).refine()
    assert cancel((x**2+5*x+6)/(x+2)) == ((x**2+5*x+6)/(x+2)).cancel()

def test_as_powers_dict():
    assert x.as_powers_dict() == {x: 1}
    assert (x**y*z).as_powers_dict() == {x: y, z: 1}
    assert Mul(2, 2, **dict(evaluate=False)).as_powers_dict() == {S(2): S(2)}

def test_as_coefficients_dict():
    check = [S(1), x, y, x*y, 1]
    assert [Add(3*x, 2*x, y, 3).as_coefficients_dict()[i] for i in check] == \
    [3, 5, 1, 0, 0]
    assert [(3*x*y).as_coefficients_dict()[i] for i in check] == \
    [0, 0, 0, 3, 0]
    assert (3.0*x*y).as_coefficients_dict()[3.0*x*y] == 1

def test_args_cnc():
    A = symbols('A', commutative=False)
    assert (x+A).args_cnc() == \
        [set([]), [x + A]]
    assert (x+a).args_cnc() == \
        [set([a + x]), []]
    assert (x*a).args_cnc() == \
        [set([x, a]), []]
    assert (x*y*A*(A+1)).args_cnc(clist=True) == \
        [[x, y], [A, 1 + A]]

def test_new_rawargs():
    n = Symbol('n', commutative=False)
    a = x + n
    assert a.is_commutative is False
    assert a._new_rawargs(x).is_commutative
    assert a._new_rawargs(x, y).is_commutative
    assert a._new_rawargs(x, n).is_commutative is False
    assert a._new_rawargs(x, y, n).is_commutative is False
    m = x*n
    assert m.is_commutative is False
    assert m._new_rawargs(x).is_commutative
    assert m._new_rawargs(n).is_commutative is False
    assert m._new_rawargs(x, y).is_commutative
    assert m._new_rawargs(x, n).is_commutative is False
    assert m._new_rawargs(x, y, n).is_commutative is False

    assert m._new_rawargs(x, n, reeval=False).is_commutative is False
    assert m._new_rawargs(S.One) is S.One

def test_2127():
    assert Add(evaluate=False) == 0
    assert Mul(evaluate=False) == 1
    assert Mul(x+y, evaluate=False).is_Add

def test_symbols():
    # symbols should return the free symbols of an object
    assert S(1).free_symbols == set()
    assert (x).free_symbols == set([x])
    assert Integral(x, (x, 1, y)).free_symbols == set([y])
    assert (-Integral(x, (x, 1, y))).free_symbols == set([y])

def test_issue2201():
    x = Symbol('x', commutative=False)
    assert x*sqrt(2)/sqrt(6) == x*sqrt(3)/3

def test_issue_2061():
    assert sqrt(-1.0*x) == 1.0*I*sqrt(x)
    assert sqrt(1.0*x) == 1.0*sqrt(x)

def test_as_coeff_Mul():
    assert Integer(3).as_coeff_Mul() == (Integer(3), Integer(1))
    assert Rational(3, 4).as_coeff_Mul() == (Rational(3, 4), Integer(1))
    assert Float(5.0).as_coeff_Mul() == (Float(5.0), Integer(1))

    assert (Integer(3)*x).as_coeff_Mul() == (Integer(3), x)
    assert (Rational(3, 4)*x).as_coeff_Mul() == (Rational(3, 4), x)
    assert (Float(5.0)*x).as_coeff_Mul() == (Float(5.0), x)

    assert (Integer(3)*x*y).as_coeff_Mul() == (Integer(3), x*y)
    assert (Rational(3, 4)*x*y).as_coeff_Mul() == (Rational(3, 4), x*y)
    assert (Float(5.0)*x*y).as_coeff_Mul() == (Float(5.0), x*y)

    assert (x).as_coeff_Mul() == (S.One, x)
    assert (x*y).as_coeff_Mul() == (S.One, x*y)

def test_as_coeff_Add():
    assert Integer(3).as_coeff_Add() == (Integer(3), Integer(0))
    assert Rational(3, 4).as_coeff_Add() == (Rational(3, 4), Integer(0))
    assert Float(5.0).as_coeff_Add() == (Float(5.0), Integer(0))

    assert (Integer(3) + x).as_coeff_Add() == (Integer(3), x)
    assert (Rational(3, 4) + x).as_coeff_Add() == (Rational(3, 4), x)
    assert (Float(5.0) + x).as_coeff_Add() == (Float(5.0), x)

    assert (Integer(3) + x + y).as_coeff_Add() == (Integer(3), x + y)
    assert (Rational(3, 4) + x + y).as_coeff_Add() == (Rational(3, 4), x + y)
    assert (Float(5.0) + x + y).as_coeff_Add() == (Float(5.0), x + y)

    assert (x).as_coeff_Add() == (S.Zero, x)
    assert (x*y).as_coeff_Add() == (S.Zero, x*y)

def test_expr_sorting():
    f, g = symbols('f,g', cls=Function)

    exprs = [1/x**2, 1/x, sqrt(sqrt(x)), sqrt(x), x, sqrt(x)**3, x**2]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [x, 2*x, 2*x**2, 2*x**3, x**n, 2*x**n, sin(x), sin(x)**n, sin(x**2), cos(x), cos(x**2), tan(x)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [x + 1, x**2 + x + 1, x**3 + x**2 + x + 1]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [S(4), x - 3*I/2, x + 3*I/2, x - 4*I + 1, x + 4*I + 1]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [f(1), f(2), f(3), f(1, 2, 3), g(1), g(2), g(3), g(1, 2, 3)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [f(x), g(x), exp(x), sin(x), cos(x), factorial(x)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [Tuple(x, y), Tuple(x, z), Tuple(x, y, z)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [[3], [1, 2]]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [[1, 2], [2, 3]]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [[1, 2], [1, 2, 3]]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [{x: -y}, {x: y}]
    assert sorted(exprs, key=default_sort_key) == exprs

def test_as_ordered_factors():
    f, g = symbols('f,g', cls=Function)

    assert x.as_ordered_factors() == [x]
    assert (2*x*x**n*sin(x)*cos(x)).as_ordered_factors() == [Integer(2), x, x**n, sin(x), cos(x)]

    args = [f(1), f(2), f(3), f(1, 2, 3), g(1), g(2), g(3), g(1, 2, 3)]
    expr = Mul(*args)

    assert expr.as_ordered_factors() == args

    A, B = symbols('A,B', commutative=False)

    assert (A*B).as_ordered_factors() == [A, B]
    assert (B*A).as_ordered_factors() == [B, A]

def test_as_ordered_terms():
    f, g = symbols('f,g', cls=Function)

    assert x.as_ordered_terms() == [x]
    assert (sin(x)**2*cos(x) + sin(x)*cos(x)**2 + 1).as_ordered_terms() == [sin(x)**2*cos(x), sin(x)*cos(x)**2, 1]

    args = [f(1), f(2), f(3), f(1, 2, 3), g(1), g(2), g(3), g(1, 2, 3)]
    expr = Add(*args)

    assert expr.as_ordered_terms() == args

    assert (1 + 4*sqrt(3)*pi*x).as_ordered_terms() == [4*pi*x*sqrt(3), 1]

    assert ( 2 + 3*I).as_ordered_terms() == [ 2,  3*I]
    assert (-2 + 3*I).as_ordered_terms() == [-2,  3*I]
    assert ( 2 - 3*I).as_ordered_terms() == [ 2, -3*I]
    assert (-2 - 3*I).as_ordered_terms() == [-2, -3*I]

    assert ( 4 + 3*I).as_ordered_terms() == [ 4,  3*I]
    assert (-4 + 3*I).as_ordered_terms() == [-4,  3*I]
    assert ( 4 - 3*I).as_ordered_terms() == [ 4, -3*I]
    assert (-4 - 3*I).as_ordered_terms() == [-4, -3*I]

    f = x**2*y**2 + x*y**4 + y + 2

    assert f.as_ordered_terms(order="lex") == [x**2*y**2, x*y**4, y, 2]
    assert f.as_ordered_terms(order="grlex") == [x*y**4, x**2*y**2, y, 2]
    assert f.as_ordered_terms(order="rev-lex") == [2, y, x*y**4, x**2*y**2]
    assert f.as_ordered_terms(order="rev-grlex") == [2, y, x**2*y**2, x*y**4]

def test_sort_key_atomic_expr():
    from sympy.physics.units import m, s
    assert sorted([-m, s], key=lambda arg: arg.sort_key()) == [-m, s]

def test_issue_1100():
    # first subs and limit gives NaN
    a = x/y
    assert a._eval_interval(x, 0, oo)._eval_interval(y, oo, 0) is S.NaN
    # second subs and limit gives NaN
    assert a._eval_interval(x, 0, oo)._eval_interval(y, 0, oo) is S.NaN
    # difference gives S.NaN
    a = x - y
    assert a._eval_interval(x, 1, oo)._eval_interval(y, oo, 1) is S.NaN
    raises(ValueError, 'x._eval_interval(x, None, None)')

def test_primitive():
    assert (3*(x + 1)**2).primitive() == (3, (x + 1)**2)
    assert (6*x + 2).primitive() == (2, 3*x + 1)
    assert (x/2 + 3).primitive() == (S(1)/2, x + 6)
    eq = (6*x + 2)*(x/2 + 3)
    assert eq.primitive()[0] == 1
    eq = (2 + 2*x)**2
    assert eq.primitive()[0] == 1
    assert (4.0*x).primitive() == (1, 4.0*x)
    assert (4.0*x + y/2).primitive() == (S.Half, 8.0*x + y)
    assert (-2*x).primitive() == (2, -x)
    assert Add(5*z/7, 0.5*x, 3*y/2, evaluate=False).primitive() == \
        (S(1)/14, 7.0*x + 21*y + 10*z)
    for i in [S.Infinity, S.NegativeInfinity, S.ComplexInfinity]:
        assert (i + x/3).primitive() == \
            (S(1)/3, i + x)
    assert (S.Infinity + 2*x/3 + 4*y/7).primitive() == \
        (S(2)/21, 7*x + 6*y + oo)
    assert S.Zero.primitive() == (S.One, S.Zero)

def test_issue_2744():
    a = 1 + x
    assert (2*a).extract_multiplicatively(a) == 2
    assert (4*a).extract_multiplicatively(2*a) == 2
    assert ((3*a)*(2*a)).extract_multiplicatively(a) == 6*a

def test_is_constant():
    from sympy.solvers.solvers import checksol
    Sum(x, (x, 1, 10)).is_constant() == True
    Sum(x, (x, 1, n)).is_constant() == False
    Sum(x, (x, 1, n)).is_constant(y) == True
    Sum(x, (x, 1, n)).is_constant(n) == False
    Sum(x, (x, 1, n)).is_constant(x) == True
    eq = a*cos(x)**2 + a*sin(x)**2 - a
    eq.is_constant() == True
    assert eq.subs({x:pi, a:2}) == eq.subs({x:pi, a:3}) == 0
    assert x.is_constant() is False
    assert x.is_constant(y) is True

    assert checksol(x, x, Sum(x, (x, 1, n))) == False
    assert checksol(x, x, Sum(x, (x, 1, n))) == False
    f = Function('f')
    assert checksol(x, x, f(x)) == False

    p = symbols('p', positive=True)
    assert Pow(x, S(0), evaluate=False).is_constant() == True # == 1
    assert Pow(S(0), x, evaluate=False).is_constant() == False # == 0 or 1
    assert Pow(S(0), p, evaluate=False).is_constant() == True # == 1
    assert (2**x).is_constant() == False
    assert Pow(S(2), S(3), evaluate=False).is_constant() == True

    z1, z2 = symbols('z1 z2', zero=True)
    assert (z1+2*z2).is_constant

@XFAIL
def test_is_not_constant():
    assert (-3 - sqrt(5) + (-sqrt(10)/2 - sqrt(2)/2)**2).is_zero != False

def test_equals():
    assert (x**2 - 1).equals((x + 1)*(x - 1))
    assert (cos(x)**2 + sin(x)**2).equals(1)
    assert (a*cos(x)**2 + a*sin(x)**2).equals(a)
    r = sqrt(2)
    assert (-1/(r + r*x) + 1/r/(1 + x)).equals(0)
    assert factorial(x + 1).equals((x + 1)*factorial(x))

@XFAIL
def test_equals_factorial():
    assert factorial(x + 1).diff(x).equals(((x + 1)*factorial(x)).diff(x))
