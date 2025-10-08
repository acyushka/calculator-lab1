import re
import operator

TOKEN_PATTERN = re.compile(r"""
                           \s*
                           (
                           \d+(?:\.\d+)?
                           |\*\*
                           |//
                           |\(\)
                           |[%()+\-*/]
                           )
                           \s*
                           """, re.VERBOSE)

OPERATIONS = {
    '+': operator.add,
    '-': operator.sub,
    '/': operator.truediv,
    '*': operator.mul,
    '**': operator.pow,
    '//': operator.floordiv,
    '%': operator.mod,
}

OPERATOR_PRECEDENCE = {
    '~': 4,
    '$': 4,
    '**': 3,
    '*': 2, '/': 2, '//': 2, '%': 2,
    '+': 1, '-': 1,
}
