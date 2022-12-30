from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.


def do_define_form(expressions, env):
    """Evaluate a define form.
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2)  # Checks that expressions is a list of length at least 2
    signature = expressions.first
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        validate_form(expressions, 2, 2)  # Checks that expressions is a list of length exactly 2
        # BEGIN PROBLEM 4
        """
        This clause targets cases like (define x (+ 1 2)), so the expression will be (x (+ 1 2)), the signature will be x, the second operands of "(define x (+ 1 2))" will be (+ 1 2). In order to bind the symbol with value, we need to use scheme_eval to evalutate the second operand. However, we can't directly take expressions.rest as input for scheme_eval. Because it will be Pair(Pair('+', Pair(1, Pair(2, nil))), nil), while what we need is Pair('+', Pair(1, Pair(2, nil))).

        Implement the scheme_read in lab11 help me understand this problem better.
        """
        env.define(signature, scheme_eval(expressions.rest.first, env))
        
        return signature
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g. (define (f x y) (+ x y))
        # BEGIN PROBLEM 10
        name = signature.first
        formals = signature.rest
        body = expressions.rest
        expr4p = Pair(formals, body)
        # print('expr4p', expr4p)
        p = do_lambda_form(expr4p, env)
        env.define(name, p)
        return name
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))


def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating (quote (+ x 2))
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    return expressions.first
    # END PROBLEM 5


def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)


def do_lambda_form(expressions, env):
    """Evaluate a lambda form.

    In Scheme, it is legal to place more than one expression in the body of a procedure. (There must be at least one expression.) The body attribute of a LambdaProcedure instance is therefore a Scheme list of body expressions.

    The formals attribute of a LambdaProcedure instance should be a properly nested Pair expression.

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating (lambda (x) (+ x 2))
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    # notice the body in the example is Pair(Pair('+', Pair('x', Pair(2, nil))), nil), so it's expressions.rest, not expressions.rest.first. Another clue is that the body will be evaluated by eval_all instead of scheme_eval because there will be multiple expressions in lambda body, so it's like a begin form.
    body = expressions.rest
    # print('formals', formals)
    p = LambdaProcedure(formals, body, env)
    return p
    # END PROBLEM 7


def do_if_form(expressions, env):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    validate_form(expressions, 2, 3)#the length of expressions is 2(only condition if-true-clause) or 3(condition if-true-clause if-false-clause)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env)


def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    For 'and', if there are no sub-expressions in an and expression, it evaluates to #t.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating (and #f (print 1))
    False
    >>> # evaluating (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    if expressions == nil:
        return True

    # expressions.first should be evalutated first then check whether it's true. And the eval function cannot be applied twice, so we assign it to tmp here.
    tmp = scheme_eval(expressions.first, env)
    if is_scheme_true(tmp):
        if len(expressions) == 1:
            return tmp
        else:
            return do_and_form(expressions.rest, env)
    return False
    # END PROBLEM 12


def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    For 'or', if there are no sub-expressions in an or expression, it evaluates to #f.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating (or #f 2 3 #t #f)
    2
    >>> # evaluating (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    if expressions == nil:
        return False
    
    tmp = scheme_eval(expressions.first, env)
    if is_scheme_true(tmp):
        return tmp
    if expressions.rest:
        return do_or_form(expressions.rest, env)
    else:
        return False
    # END PROBLEM 12


def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            if len(clause) == 1:
                return test
            return eval_all(clause.rest, env)
            # END PROBLEM 13
        expressions = expressions.rest


def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)


def make_let_frame(bindings, env):
    """Create a child frame of Frame ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN PROBLEM 14
    def helper(my_pair):
        if my_pair == nil:
            return nil, nil
        validate_form(my_pair.first, 2, 2)
        return Pair(my_pair.first.first, helper(my_pair.rest)[0]), Pair(scheme_eval(my_pair.first.rest.first, env), helper(my_pair.rest)[1])
        
    names, vals = helper(bindings)
    validate_formals(names) # this function validates that its argument is a Scheme list of symbols for which each symbol is distinct.
    # END PROBLEM 14
    return env.make_child_frame(names, vals)


def do_define_macro(expressions, env):
    """Evaluate a define-macro form.

    >>> env = create_global_frame()
    >>> do_define_macro(read_line("((f x) (car x))"), env)
    'f'
    >>> scheme_eval(read_line("(f (1 2))"), env)
    1
    """
    # BEGIN PROBLEM OPTIONAL_1
    "*** YOUR CODE HERE ***"
    # END PROBLEM OPTIONAL_1


def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    Frame ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in Frame ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)


def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# Dynamic Scope #
#################
"""
All of the Scheme procedures we've seen so far use **lexical scoping**: the parent of the new call frame is the environment in which the procedure was defined. 

Another type of scoping, which is not standard in Scheme but appears in other variants of Lisp, is called **dynamic scoping**: the parent of the new call frame is the environment in which the call expression was evaluated. 

"""

def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    body = expressions.rest
    return MuProcedure(formals, body)
    # END PROBLEM 11


SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'define-macro': do_define_macro,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}
