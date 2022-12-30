import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

#my
from scheme_builtins import *

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR **in Frame ENV**.

    >>> expr = read_line('(+ 2 2)') # read_line is implemented in lab11, completing the "read" step in "read-eval-print" pipeline.
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):#string, but not starts with '"'
        return env.lookup(expr)
    elif self_evaluating(expr):#self
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))

    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        """
        do not mutate the passed-in expr. That would change a program as it's being evaluated, creating strange and incorrect effects.
        """
        try:
            # only evaluate the operator of a call expression once in scheme_eval.
            eval_operator = scheme_eval(first, env) # now the expression is atomic, so the first if clause will be implemented to lookup "first"
            eval_operands = rest # in order to avoid mutation of expr
            eval_operands = eval_operands.map(lambda x: scheme_eval(x, env)) #Pair has a map method
            return scheme_apply(eval_operator, eval_operands, env)
        except:
            raise SchemeError


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment.
    
    args is a list of argument values
    """
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        """ Built-in procedures are applied by calling a corresponding Python function that implements the procedure."""
        # BEGIN PROBLEM 2
        lst = []
        while args:
            lst.append(args.first)
            args = args.rest
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            if procedure.need_env:
                return procedure.py_func(*lst, env)
            else:
                return procedure.py_func(*lst)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        """
        scm> (define square (lambda (x) (* x x)))
        square
        scm> square
        (lambda (x) (* x x))
        scm> (square 21)
        441
        """
        # BEGIN PROBLEM 9
        try:
            formals = procedure.formals
            body = procedure.body
            """
            Note that the env provided as an argument to scheme_apply is instead the frame in which the procedure is called. 
            
            So don't use env.make_child_frame here
            """
            new_frame = procedure.env.make_child_frame(formals, args)
            return eval_all(body, new_frame)
        except:
            raise SchemeError
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        try:
            formals = procedure.formals
            body = procedure.body
            new_frame = env.make_child_frame(formals, args)
            return eval_all(body, new_frame)
        except:
            raise SchemeError
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    it is called from do_begin_form in scheme_forms.py) to complete the implementation of the begin special form.
    The value of the begin expression is the value of the final sub-expression.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    res = None
    ptr = expressions
    while ptr:
        res = scheme_eval(ptr.first, env)
        ptr = ptr.rest

    return res
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
