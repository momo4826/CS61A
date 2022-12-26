def count(f):
    """Count how many times the recursive function runs"""
    def counted(n):
        counted.call_count += 1
        return f(n)
    counted.call_count = 0
    return counted

def memo(f):
    cache = {}
    def memorized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memorized

@count
@memo
def fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n-2) + fib(n-1)


def a():
    pass

a.publish = 1
a.unittest = '''...'''


class C:
    def a(self):
        'just a docstring'
        a.publish = 1

# c = C()
# if c.a.publish: # raise error, class C's method a doesn't have attribute `publish`
#     print((c.a()))



from lab09 import *
# print('hello')
# for partition in partition_gen(4): # note: order doesn't matter
#     print(partition)


# a = [1, 1, 3, 2, 1, 1, 4]
# b = [4, 3, 2, 7]
# print(trade(a, b))
# print(a)
# print(b)

# suits = ['H', 'D', 'S', 'C']
# cards = [card(n) + suit for n in range(1,14) for suit in suits]
# print(cards)


# link = Link(1, Link(2, Link(3)))
# print(link)
# insert(link, 9001, 0)
# print(link)
# insert(link, 100, 2)
# print(link)


levels = Link(Link(Link(1, Link(2)), Link(3)), Link(Link(4), Link(5)))
print(deep_len(levels))