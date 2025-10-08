from src.tokenizer import Token, CalcError


def validate_two_operators(tokens: list[Token]) -> None:
    """
    Валидатор двух идущих подряд операторов
    :param tokens: список из токенов
    :return: ничего не возвращает
    """
    for i in range(len(tokens)-2):
        if (tokens[i][0] == "OP" and tokens[i+1][0] == "OP" and
                tokens[i][1] != "(" and tokens[i+1][1] != ")"):
            raise CalcError("Два оператора не могут идти подряд!")


def validate_expr_struct(tokens: list[Token]) -> None:
    """
    Валидатор операторов на концах выражения
    :param tokens: список из токенов
    :return: ничего не возвращает
    """
    first_token: Token = tokens[0]
    last_token: Token = tokens[-2]

    if (first_token[0] == "OP" and
            first_token[1] not in ("~", "$", "(")):
        raise CalcError("Выражение не может начинаться с бинарного оператора")

    if (last_token[0] == "OP" and
            last_token[1] not in (")", "~", "$")):
        raise CalcError("Выражение не может заканчиваться оператором")


def validate_brackets(tokens: list[Token]) -> None:
    """
    Валидатор правильности написания скобок, а также пустых скобок
    :param tokens: список из токенов
    :return: ничего не возвращает
    """
    # 1 часть: валидация правильности расстановки скобок через стек
    stack: list[Token] = []

    for token in tokens:
        token_type, value = token
        if token_type == "OP":
            if value == "(":
                stack.append(token)
            elif value == ")":
                try:
                    stack.pop()
                except IndexError:
                    raise CalcError("Несбалансированные скобки")
    if stack:
        raise CalcError("Несбалансированные скобки")
    # 2 часть: проверяем, что нет пустых скобок
    for i in range(len(tokens) - 2):
        if (tokens[i][0] == "OP" and tokens[i][1] == "(" and
                tokens[i+1][0] == "OP" and tokens[i+1][1] == ")"):
            raise CalcError("Пустые скобки в выражении")
