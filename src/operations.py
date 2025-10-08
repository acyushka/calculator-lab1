from src.constants import OPERATIONS


def binary_operation(operator: str, first_number: float, second_number: float) -> float:
    """
    Функция для выполнения математических операций, поддерживаемых в калькуляторе
    Вычисления производятся с помощью библиотеки operator
    :param operator: Символ операции
    :param first_number: Первое число
    :param second_number: Второе число
    :return: Возвращает итог проведенной операции над 2 числами
    """
    return OPERATIONS[operator](first_number, second_number)
