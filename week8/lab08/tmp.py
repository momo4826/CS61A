
# class Link:
#     empty = ()
#     def __init__(self, first, rest = empty):
#         assert rest is Link.empty or isinstance(rest, Link)
#         self.first = first
#         self.rest = rest

#     # def __repr__(self):
#     #     if self is Link.empty:
#     #         return "()"
#     #     return "Link({0}, {1})".format(self.first, self.rest.__repr__())
#     def __repr__(self):
#         # no need to consider Link.empty, because it's () and set has its own __repr__
#         if self.rest is Link.empty:
#             rest_repr = ""
#         else:
#             rest_repr = ", " +  self.rest.__repr__()
#         return "Link(" + repr(self.first) + rest_repr + ")"

# def add(llist, x):
#     """ordered linked list without repeating"""
#     if llist is Link.empty:
#         return Link(x)
#     elif x < llist.first:
#         llist.first, llist.rest = x, Link(llist.first, llist.rest) # it's `Link(llist.first, llist.rest)` instead of s, consider pointer(in python assignment a to b means b is just another name of a, it;s like pointer assignment is C. To discarding this connection, you need to create a new instance then assign. That's the danger of mutable objects.)
#     elif x > llist.first:
#         llist = Link(llist.first, add(llist.rest, x))
#     return llist

from lab08 import *
t = Tree(1,[Tree(3), Tree(5)])
cumulative_mul(t)
print(t)