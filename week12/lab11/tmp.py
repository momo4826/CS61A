from buffer import *
from scheme_reader import *

#print(repr(read_tail(Buffer(tokenize_lines(['2 (3 4))'])))))
print(repr(read_tail(Buffer(tokenize_lines(['(1 2 3)'])))))