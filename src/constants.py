import re

SAMPLE_CONSTANT: int = 10
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
OPERATOR_PRECEDENCE = {
    '~': 4,
    '$': 4,
    '**': 3,
    '*': 2, '/': 2, '//': 2, '%': 2,
    '+': 1, '-': 1,
}
