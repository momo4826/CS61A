from scheme import *
from scheme_builtins import *
from scheme_reader import *
from scheme_utils import *
from scheme_classes import *
from scheme_eval_apply import *
from scheme_forms import *


env = create_global_frame()


# Problem 2
# env = create_global_frame()
# twos = Pair(2, Pair(2, nil))
# plus = BuiltinProcedure(scheme_add)
# print(scheme_apply(plus, (twos), env))




#Problem 3
#print(list(filter(lambda x: x[0] == "+", BUILTINS)))


# expr = read_line('(+ 1 2)')
# print(scheme_eval(expr, env))
# expr = read_line('((print-then-return 1 +) 1 2)')
# print(scheme_eval(expr, env))
# expr = read_line('(* 3 4 (- 5 2) 1)')
# print(scheme_eval(expr, env))
# expr = read_line('(odd? 31)')
# print(scheme_eval(expr, env))


# Problem4
# expr = read_line("(x (+ 1 2))")
# print(repr(expr.rest))
# expr = read_line("(size 2)")
# expr = read_line('(y (* 2 3))')
# # print(scheme_eval(expr.rest.first, env))
# print(do_define_form(expr, env))
# print(env.lookup('y'))

#Problem5
# print(read_line("((+ x 2))"))


# Problem 7
# env = create_global_frame()
# lambda_line = read_line("(lambda (a b c) (+ a b c))")
# print(lambda_line)
# print(lambda_line.rest)
# lambda_proc = do_lambda_form(lambda_line.rest, env)
# lambda_proc # use single quotes ' around strings in your answer

# env = create_global_frame()
# lambda_line = read_line("(define outer-func (lambda (x y)(define inner (lambda (z x)(+ x (* y 2) (* z 3))))inner))")
# lambda_proc = do_lambda_form(lambda_line.rest, env)
# print(scheme_apply(lambda_proc, (twos), env))


# scm> ((apply-twice double) 5)
#           20
# scm> (do-twice double 3)
#           12

# x = Pair(2, Pair(3, nil))
# y = x
# y = y.rest
# print(repr(x))
# print(repr(y))

# Problem 12
expr = read_line('(let ((x 5))(+ x 3))')
print(scheme_eval(expr, env))