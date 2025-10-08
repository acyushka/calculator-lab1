import pytest

from src.tokenizer import tokenize, CalcError


def test_empty_input():
    """Тест пустого ввода"""
    with pytest.raises(CalcError, match="Пустой ввод"):
        tokenize("")
    with pytest.raises(CalcError, match="Пустой ввод"):
        tokenize("   ")


def test_two_numbers():
    """Тест ввода 2 чисел подряд"""
    with pytest.raises(CalcError, match="Два числа"):
        tokenize("2 222")
    with pytest.raises(CalcError, match="Два числа"):
        tokenize("2 + 2 * 6     666666")


@pytest.mark.parametrize("expression,expected", [
    ("0", [("NUM", 0.0), ("EOF", "EOF")]),
    ("1", [("NUM", 1.0), ("EOF", "EOF")]),
    ("9", [("NUM", 9.0), ("EOF", "EOF")]),
    ("10", [("NUM", 10.0), ("EOF", "EOF")]),
    ("123", [("NUM", 123.0), ("EOF", "EOF")]),
    ("9999", [("NUM", 9999.0), ("EOF", "EOF")]),
    ("1000000", [("NUM", 1000000.0), ("EOF", "EOF")]),
    ("123456789", [("NUM", 123456789.0), ("EOF", "EOF")]),
    ("2147483647", [("NUM", 2147483647.0), ("EOF", "EOF")]),
])
def test_integers(expression, expected):
    """Тест целых чисел"""
    result = tokenize(expression)
    assert result == expected


@pytest.mark.parametrize("expression,expected", [
    ("0.0", [("NUM", 0.0), ("EOF", "EOF")]),
    ("0.5", [("NUM", 0.5), ("EOF", "EOF")]),
    ("1.0", [("NUM", 1.0), ("EOF", "EOF")]),
    ("123.456", [("NUM", 123.456), ("EOF", "EOF")]),
    ("0.001", [("NUM", 0.001), ("EOF", "EOF")]),
    ("999.999", [("NUM", 999.999), ("EOF", "EOF")]),
    ("3.14159265359", [("NUM", 3.14159265359), ("EOF", "EOF")]),
    ("2.71828182846", [("NUM", 2.71828182846), ("EOF", "EOF")]),
    ("0.123456789", [("NUM", 0.123456789), ("EOF", "EOF")]),
    ("0.0000001", [("NUM", 0.0000001), ("EOF", "EOF")]),
    ("999999.999999", [("NUM", 999999.999999), ("EOF", "EOF")]),
    ("123456.789012", [("NUM", 123456.789012), ("EOF", "EOF")]),
])
def test_float_numbers(expression, expected):
    """Тест вещественных чисел"""
    result = tokenize(expression)
    assert result == expected


@pytest.mark.parametrize("expression,expected", [
    # Числа с унарными операторами
    ("-0", [("OP", "~"), ("NUM", 0.0), ("EOF", "EOF")]),
    ("-1", [("OP", "~"), ("NUM", 1.0), ("EOF", "EOF")]),
    ("-123.45", [("OP", "~"), ("NUM", 123.45), ("EOF", "EOF")]),
    ("+0.5", [("OP", "$"), ("NUM", 0.5), ("EOF", "EOF")]),
    ("+999", [("OP", "$"), ("NUM", 999.0), ("EOF", "EOF")]),

    # Комбинации унарных операторов с числами
    ("-1 + (-2.5)", [("OP", "~"), ("NUM", 1.0), ("OP", "+"), ("OP", "("), ("OP", "~"),
                     ("NUM", 2.5), ("OP", ")"), ("EOF", "EOF")]),
    ("+3.14 * (-2)", [("OP", "$"), ("NUM", 3.14), ("OP", "*"), ("OP", "("), ("OP", "~"),
                      ("NUM", 2.0), ("OP", ")"), ("EOF", "EOF")]),
    ("-0.5 - (+0.25)", [("OP", "~"), ("NUM", 0.5), ("OP", "-"), ("OP", "("), ("OP", "$"),
                        ("NUM", 0.25), ("OP", ")"), ("EOF", "EOF")]),
])
def test_unary_operators(expression, expected):
    """Тест ввода с унарными"""
    result = tokenize(expression)
    assert result == expected


@pytest.mark.parametrize("expression,error_pattern", [
    (".", "Некорректный ввод около:"),
    (".5", "Некорректный ввод около:"),
    (".5.", "Некорректный ввод около:"),
    ("123.", "Некорректный ввод около:"),
    ("12.34.56", "Некорректный ввод около:"),
    ("12..34", "Некорректный ввод около:"),
    ("12...56", "Некорректный ввод около:"),
    ("1,5", "Некорректный ввод около:"),
    ("0x1F", "Некорректный ввод около:"),
    ("0b101111", "Некорректный ввод около:"),
    ("1e5", "Некорректный ввод около:"),
])
def test_invalid_numbers(expression, error_pattern):
    """Тест некорректных вводов"""
    with pytest.raises(CalcError, match=error_pattern):
        tokenize(expression)


@pytest.mark.parametrize("expression,expected", [
    # Все бинарные операторы с числами
    ("2 + 3.0", [("NUM", 2.0), ("OP", "+"), ("NUM", 3.0), ("EOF", "EOF")]),
    ("5 - 2.0", [("NUM", 5.0), ("OP", "-"), ("NUM", 2.0), ("EOF", "EOF")]),
    ("3 * 4.0", [("NUM", 3.0), ("OP", "*"), ("NUM", 4.0), ("EOF", "EOF")]),
    ("8 / 2.0", [("NUM", 8.0), ("OP", "/"), ("NUM", 2.0), ("EOF", "EOF")]),
    ("7 // 2.0", [("NUM", 7.0), ("OP", "//"),
                  ("NUM", 2.0), ("EOF", "EOF")]),
    ("7 % 3.0", [("NUM", 7.0), ("OP", "%"), ("NUM", 3.0), ("EOF", "EOF")]),
    ("2 ** 3.0", [("NUM", 2.0), ("OP", "**"),
                  ("NUM", 3.0), ("EOF", "EOF")]),

    # Выражения посложнее
    ("2 + 3 * 4", [
        ("NUM", 2.0), ("OP", "+"), ("NUM", 3.0), ("OP", "*"), ("NUM", 4.0),
        ("EOF", "EOF")
    ]),
    ("(2 + 3) * 4", [
        ("OP", "("), ("NUM", 2.0), ("OP", "+"), ("NUM", 3.0), ("OP", ")"),
        ("OP", "*"), ("NUM", 4.0), ("EOF", "EOF")
    ]),
    ("2 ** 3 + 1", [
        ("NUM", 2.0), ("OP", "**"), ("NUM", 3.0), ("OP", "+"), ("NUM", 1.0),
        ("EOF", "EOF")
    ]),
    ("10.0 // 3 % 2", [
        ("NUM", 10.0), ("OP", "//"), ("NUM", 3.0), ("OP", "%"), ("NUM", 2.0),
        ("EOF", "EOF")
    ]),
    ("(201 + 33.7) * (41 - 1) // 2", [
        ("OP", "("), ("NUM", 201.0), ("OP", "+"), ("NUM", 33.7), ("OP", ")"),
        ("OP", "*"), ("OP", "("), ("NUM", 41.0), ("OP", "-"), ("NUM", 1.0),
        ("OP", ")"), ("OP", "//"), ("NUM", 2.0), ("EOF", "EOF")
    ]),
    ("258 ** 3 + 5.2 * 2 - 10 // 3", [
        ("NUM", 258.0), ("OP", "**"), ("NUM", 3.0), ("OP", "+"), ("NUM", 5.2),
        ("OP", "*"), ("NUM", 2.0), ("OP", "-"), ("NUM", 10.0), ("OP", "//"),
        ("NUM", 3.0), ("EOF", "EOF")
    ]),
    ("-5.787 + 3 * (2 ** 2) % 3", [
        ("OP", "~"), ("NUM", 5.787), ("OP", "+"), ("NUM", 3.0), ("OP", "*"),
        ("OP", "("), ("NUM", 2.0), ("OP", "**"), ("NUM", 2.0), ("OP", ")"),
        ("OP", "%"), ("NUM", 3.0), ("EOF", "EOF")
    ]),
    ("10.5 // 2.5 + 3.5 * 2.0 - 5.5 % 2.0", [
        ("NUM", 10.5), ("OP", "//"), ("NUM", 2.5), ("OP", "+"), ("NUM", 3.5),
        ("OP", "*"), ("NUM", 2.0), ("OP", "-"), ("NUM", 5.5), ("OP", "%"),
        ("NUM", 2.0), ("EOF", "EOF")
    ]),
    ("(((((-5 + 6)))))", [
        ("OP", "("), ("OP", "("), ("OP", "("), ("OP", "("), ("OP", "("),
        ("OP", "~"), ("NUM", 5.0), ("OP", "+"), ("NUM", 6.0), ("OP", ")"),
        ("OP", ")"), ("OP", ")"), ("OP", ")"), ("OP", ")"), ("EOF", "EOF")
    ])
])
def test_expressions(expression, expected):
    """Тест сложных выражений"""
    result = tokenize(expression)
    assert result == expected
