from src.tokenizer import tokenize
from src.converter import convert_to_rpn
from src.rpn_calculate import calculate_rpn


def test_expressions_full():
    """Тест выражений полным циклом"""

    cases = [
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("2 ** 3 ** 2", 512),
        ("-5 + 3", -2),
        ("5 + (-3) * 2", -1),
        ("10 //   3 + 7 % 4", 6),
        ("2.5 * (3 + 1.5)", 11.25),
        ("-2 ** (+3) * (5 - (-1))", -48),
        ("((2 + 3) * 4 - 1) // 2", 9),
        ("0.5 + 0.25 * 2", 1),
        ("2 * 3 + 4 * 5 - 6 / 2", 23),
        ("(1 + 2) ** (1 + 2)", 27),
    ]

    for expression, expected in cases:
        tokens = tokenize(expression)
        rpn_expr = convert_to_rpn(tokens)
        result = calculate_rpn(rpn_expr)
        assert result == expected
