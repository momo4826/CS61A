

# https://stackoverflow.com/questions/13467674/determining-complexity-for-recursive-functions-big-o-notation
def count(f):
    def counted(*arg):
        counted.call_count += 1
        return f(*arg)
    counted.call_count = 0
    return counted


def f1(n:'integer')->'integer':
    """O(n)
    T(n) = a + T(n - 1), By induction T(n) = n * a + T(0) = n * a + b = O(n)"""
    if n <= 0:
        return 1
    else:
        return 1 + f1(n-1)

@count
def f2(n):
    """O(log(n))
    T(n) = a + T(n / 5), By induction T(n) = a * log5(n) + T(0) = a * log5(n) + b = O(log n)"""
    if n <= 0:
        return 1
    else:
        return 1 + f1(n/5)

@count
def f3(n, m):
    """count partitions, O(constant^n)
    recursive tree is exponential"""
    if n == 0:
        return 1
    elif n < 0:
        return 0
    elif m == 0:
        return 0
    else:
        with_m = f3(n-m, m)
        without_m = f3(n, m-1)
        return with_m + without_m


@count
def f4(n):
    """O(n^2)"""
    tmp = 0
    for i in range(n):
        tmp += i # it can be replaced with anything, doesn't matter
    if n <= 0:
        return 1
    else:
        return 1 + f4(n-1)

@count
def f5(n):
    tmp = 0
    for i in range(n):
        tmp += i # it can be replaced with anything, doesn't matter
    if n <= 0:
        return 1
    else:
        return 1 + f5(n/2)