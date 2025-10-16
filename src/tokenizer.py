from src.constants import TOKEN_PATTERN


class CalcError(Exception):
    """Понятные ошибки калькулятора"""
    pass


Token = tuple[str, float | str]


def tokenize(expr: str) -> list[Token]:
    """
    Токенизатор разбивает его на токены введенное выражение
    Токен - кортеж из 2 элементов: тип токена(str), содержимое(float если число, иначе str)
    Токенами могут быть числа, операции(скобки тоже) и пометка конца строки(EOF)
    :param expr: выражение типа str
    :return: список токенов
    """
    if not expr.strip():
        raise CalcError("Пустой ввод")

    pos = 0
    rpn_expr: list[Token] = []

    while pos < len(expr):
        m = TOKEN_PATTERN.match(expr, pos)
        if not m:
            raise CalcError(f"Некорректный ввод около: '{expr[pos]}'")

        t = m.group(1)
        pos = m.end()

        if t[0].isdigit():
            # ловим ввод двух чисел подряд
            if rpn_expr and rpn_expr[-1][0] == "NUM":
                raise CalcError("Два числа не могут идти подряд!")
            rpn_expr.append(("NUM", float(t)))

        elif t in ('+', '-'):  # обрабатываем унарные как операции
            if not rpn_expr:
                if t == '-':
                    rpn_expr.append(("OP", "~"))
                else:
                    rpn_expr.append(("OP", "$"))

            elif rpn_expr[-1][-1] == '(':
                if t == '-':
                    rpn_expr.append(("OP", "~"))
                else:
                    rpn_expr.append(("OP", "$"))

            else:
                rpn_expr.append(("OP", t))

        else:
            rpn_expr.append(("OP", t))

    rpn_expr.append(("EOF", "EOF"))
    return rpn_expr
