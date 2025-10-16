from src.tokenizer import Token, CalcError
from src.operations import binary_operation as operation


def calculate_rpn(rpn_expr: list[Token]) -> float | int:
    """
    Функция подсчитывает RPN-выражение
    :param tokens: список токенов
    :return: ответ на выражение пользователя
    """
    stack = []

    for token in rpn_expr:
        token_type, value = token

        if token_type == "NUM":
            # костыль для mypy
            if isinstance(value, float):
                number: float = value
            stack.append(number)

        elif token_type == "OP":
            if isinstance(value, str):
                value_op: str = value

            if value_op in ("~", "$"):
                try:
                    result = stack.pop()
                except IndexError:
                    raise CalcError("Выражение введено неверно")

                if value_op == "~":
                    stack.append(-result)
                else:
                    stack.append(+result)

            else:
                if len(stack) < 2:
                    raise CalcError("Выражение введено неверно")

                b = stack.pop()
                a = stack.pop()

                if value_op == "/":
                    if b != 0:
                        result = operation(value_op, a, b)
                    else:
                        raise CalcError("Делить на ноль нельзя!")

                elif value_op in ("//", "%"):
                    if b == 0:
                        raise CalcError("Делить на ноль нельзя!")

                    if a.is_integer() and b.is_integer():
                        result = operation(value_op, a, b)
                    else:
                        raise CalcError(
                            f"Операция {value} поддерживает только целые числа"
                        )

                elif value_op == "**":
                    try:
                        result = operation(value_op, a, b)
                        if isinstance(result, complex):
                            raise CalcError(
                                "В результате вычислений возникло комплексное число"
                            )

                    except OverflowError:
                        raise CalcError(
                            "Переполнение при возведении в степень"
                        )

                    except ZeroDivisionError:
                        raise CalcError("Делить на ноль нельзя")

                    except ValueError:
                        raise CalcError("Некорректное возведение в степень")

                else:
                    result = operation(value_op, a, b)
                stack.append(result)

    if len(stack) != 1:
        raise CalcError("Выражение введено неверно")

    output: float = stack[0]
    if output.is_integer():
        return int(output)

    return output
