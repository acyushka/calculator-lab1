import pytest

from src.tokenizer import CalcError
from src.rpn_calculate import calculate_rpn


@pytest.mark.parametrize("tokens,expected", [
    ([("NUM", 5.0), ("OP", "~")], -5),
    ([("NUM", 3.0), ("OP", "$")], 3),
    ([("NUM", 2.0), ("NUM", 3.0), ("OP", "+")], 5),
    ([("NUM", 5.0), ("NUM", 2.0), ("OP", "-")], 3),
    ([("NUM", 3.0), ("NUM", 4.0), ("OP", "*")], 12),
    ([("NUM", 8.0), ("NUM", 2.0), ("OP", "/")], 4),
    ([("NUM", 2.0), ("NUM", 3.0), ("OP", "**")], 8),
    ([("NUM", 4.0), ("NUM", 0.5), ("OP", "**")], 2),
    ([("NUM", 10.0), ("NUM", 3.0), ("OP", "//")], 3),
    ([("NUM", 7.0), ("NUM", 3.0), ("OP", "%")], 1),
    ([("NUM", 2.0), ("NUM", 3.0), ("NUM", 4.0), ("OP", "*"), ("OP", "+")], 14.0),
    ([("NUM", 2.0), ("NUM", 3.0), ("OP", "+"), ("NUM", 4.0), ("OP", "*")], 20.0),
    ([("NUM", 10.0), ("NUM", 3.0), ("OP", "//"), ("NUM", 2.0), ("OP", "%")], 1.0),
    ([("NUM", 17.0), ("NUM", 5.0), ("OP", "//"), ("NUM", 3.0), ("OP", "*")], 9.0),
    ([("NUM", 20.0), ("NUM", 6.0), ("OP", "%"), ("NUM", 2.0), ("OP", "+")], 4.0),
    ([("NUM", 2.0), ("OP", "~"), ("NUM", 3.0), ("OP", "*")], -6.0),
])
def test_basic_operations(tokens, expected):
    """Тест базовых операций"""
    result = calculate_rpn(tokens)
    assert result == expected


@pytest.mark.parametrize("tokens,error_pattern", [
    # Операции // и % с вещественными числами
    ([("NUM", 10.5), ("NUM", 3.0), ("OP", "//")], "только целые числа"),
    ([("NUM", 7.0), ("NUM", 3.5), ("OP", "%")], "только целые числа"),
    ([("NUM", 10.1), ("NUM", 2.0), ("OP", "//")], "только целые числа"),
    ([("NUM", 5.0), ("NUM", 2.5), ("OP", "%")], "только целые числа"),

    # Деление на ноль
    ([("NUM", 5.0), ("NUM", 0.0), ("OP", "/")], "на ноль"),
    ([("NUM", 10.0), ("NUM", 0.0), ("OP", "//")], "на ноль"),
    ([("NUM", 7.0), ("NUM", 0.0), ("OP", "%")], "на ноль"),
])
def test_exceptions(tokens, error_pattern):
    """Тест ошибок в выражениях с //, /, %"""
    with pytest.raises(CalcError, match=error_pattern):
        calculate_rpn(tokens)


@pytest.mark.parametrize("tokens,error_pattern", [
    # OverflowError
    ([("NUM", 10.0), ("NUM", 1000.0), ("OP", "**")], "Переполнение"),
    ([("NUM", 999999.0), ("NUM", 999999.0), ("OP", "**")], "Переполнение"),

    # ZeroDivisionError
    ([("NUM", 0.0), ("NUM", -1.0), ("OP", "**")], "Делить на ноль"),

    # Образование комплексных чисел
    ([("NUM", -1.0), ("NUM", 0.5), ("OP", "**")], "комплексное число"),
    ([("NUM", -4.0), ("NUM", 2.5), ("OP", "**")], "комплексное число"),
    ([("NUM", -2.0), ("NUM", 1.5), ("OP", "**")], "комплексное число"),
])
def test_power_errors(tokens, error_pattern):
    """Тест ошибок при возведении в степень"""
    with pytest.raises(CalcError, match=error_pattern):
        calculate_rpn(tokens)
