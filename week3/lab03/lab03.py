from operator import add, mul

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


def ordered_digits(x):
    """Return True if the (base 10) digits of X>0 are in non-decreasing
    order, and False otherwise.

    >>> ordered_digits(5)
    True
    >>> ordered_digits(11)
    True
    >>> ordered_digits(127)
    True
    >>> ordered_digits(1357)
    True
    >>> ordered_digits(21)
    False
    >>> result = ordered_digits(1375) # Return, don't print
    >>> result
    False

    """
    while x:
        if x % 10 < x // 10 % 10:
            return False
        x = x // 10
    return True


def get_k_run_starter(n, k):
    """Returns the 0th digit of the kth increasing run within n.
    >>> get_k_run_starter(123444345, 0) # example from description
    3
    >>> get_k_run_starter(123444345, 1)
    4
    >>> get_k_run_starter(123444345, 2)
    4
    >>> get_k_run_starter(123444345, 3)
    1
    >>> get_k_run_starter(123412341234, 1)
    1
    >>> get_k_run_starter(1234234534564567, 0)
    4
    >>> get_k_run_starter(1234234534564567, 1)
    3
    >>> get_k_run_starter(1234234534564567, 2)
    2
    """
    cnt = 0
    while n:
        if n % 10 <= n // 10 % 10 or n - n%10 == 0:
            if k == cnt:
                return n%10
            else:
                cnt += 1
        n //= 10

    return None


    # i = 0
    # final = None
    # while ____________________________:
    #     while ____________________________:
    #         ____________________________
    #     final = ____________________________
    #     i = ____________________________
    #     n = ____________________________
    # return final


def make_repeater(func, n):
    """Return the function that computes the nth application of func.

    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times!
    5
    """
    def apply_repeater(x):
        if n == 0:
            return x 
        elif n == 1:
            return func(x)
        else:
            return func(make_repeater(func, n-1)(x))
    return apply_repeater


def composer(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f


def apply_twice(func):
    """ Return a function that applies func twice.

    func -- a function that takes one argument

    >>> apply_twice(square)(2)
    16
    """
    return make_repeater(func, 2)


def div_by_primes_under(n):
    """
    >>> div_by_primes_under(10)(11)
    False
    >>> div_by_primes_under(10)(121)
    False
    >>> div_by_primes_under(10)(12)
    True
    >>> div_by_primes_under(5)(1)
    False
    """
    checker = lambda x: False
    for i in range(2, n+1):
        # My first try, RecursionError: maximum recursion depth exceeded in comparison
        # checker = lambda x: x % i == 0 or checker(x)
        # My second try, error div_by_primes_under(10)(12) -> False
        #checker = (lambda f: lambda x: x % i ==0 or f(x))(checker)
        # The right one
        checker = (lambda f, i: lambda x: x % i == 0 or f(x))(checker, i)
    return checker
    
    # checker = lambda x: False
    # i = ____________________________
    # while ____________________________:
    #     if not checker(i):
    #         checker = ____________________________
    #     i = ____________________________
    # return ____________________________


def div_by_primes_under_no_lambda(n):
    """
    >>> div_by_primes_under_no_lambda(10)(11)
    False
    >>> div_by_primes_under_no_lambda(10)(121)
    False
    >>> div_by_primes_under_no_lambda(10)(12)
    True
    >>> div_by_primes_under_no_lambda(5)(1)
    False
    """
    def checker(k):
        for i in range(2, n+1):
            if k % i == 0:
                return True 
        return False
    return checker
    # def checker(x):
    #     return False
    # i = ____________________________
    # while ____________________________:
    #     if not checker(i):
    #         def outer(____________________________):
    #             def inner(____________________________):
    #                 return ____________________________
    #             return ____________________________
    #         checker = ____________________________
    #     i = ____________________________
    # return ____________________________


def zero(f):
    return lambda x: x


def successor(n):
    return lambda f: lambda x: f(n(f)(x))


# lambda f: lambda x: f(zero(f)(x))
# =lambda f: lambda x: f(x)
def one(f):
    """Church numeral 1: same as successor(zero)"""
    return lambda x: f(x)

#print(successor(zero)(increment)(1))

def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    return lambda x: f(f(x))
#print(successor(two)(increment)(1))

three = successor(two)

def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    return n(increment)(0) 

#print(church_to_int(two))

def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    i, j = church_to_int(m), church_to_int(n)
    sum = i + j
    res = zero
    while sum:
        res = successor(res)
        sum -= 1
    return res

def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    cnt = church_to_int(m)
    res = zero
    while cnt:
        res = add_church(res, n)
        cnt -= 1
    return res


def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    cnt = church_to_int(n)
    res = one
    while cnt:
        res = mul_church(res, m)
        cnt -= 1
    return res
