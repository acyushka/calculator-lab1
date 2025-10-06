from src.constants import TOKEN_PATTERN


class CalcError(Exception):
    pass


# TOKEN_RE = re.compile(r"\s*(\d+(?:\.\d+)?|[+\-*/])")


Token = tuple[str, float | str]


def tokenize(expr: str) -> list[Token]:
    """
    Функция, реализующая токенизатор: принимает введенное в виде строки выражение, разбивает его на токены.
    Токен - это кортеж из 2 элементов: тип токена(str), содержимое(float если число, иначе str)
    Токенами могут быть числа, операции(скобки тоже) и пометка конца строки(EOF).
    Здесь же реализовано определение унарных операторов на основе контекста.
    Функция возвращает список токенов.
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
            # валидатор ведущих нулей
            # валидатор двух чисел подряд
            rpn_expr.append(("NUM", float(t)))

        elif t in ('+', '-'):
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
