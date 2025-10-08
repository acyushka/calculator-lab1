from src.tokenizer import Token
from src.constants import OPERATOR_PRECEDENCE


def convert_to_rpn(tokens: list[Token]) -> list[Token]:
    """
    Функция преобразует инфиксное выражение, разбитое на токены, в RPN по алгоритму Дейкстры.
    :param tokens: список токенов в исходном порядке
    :return: список токенов в порядке RPN
    """
    stack = []
    output = []
    for token in tokens:
        token_type, value = token

        if token_type == "NUM":
            output.append(token)
        elif token_type == "OP":
            if isinstance(value, str):
                value_op: str = value
            op_token = (token_type, value_op)
            if value_op == "(":
                stack.append(op_token)
            elif value_op in ("~", "$"):
                stack.append(op_token)
            elif value_op == "**":  # т.к. право-ассоц. оператор: в условии строго <
                while (stack and stack[-1][-1] != '(' and
                        OPERATOR_PRECEDENCE[value_op] < OPERATOR_PRECEDENCE[stack[-1][-1]]):
                    output.append(stack.pop())
                stack.append(op_token)
            elif value_op in OPERATOR_PRECEDENCE:
                while (stack and stack[-1][-1] != '(' and
                       OPERATOR_PRECEDENCE[value_op] <= OPERATOR_PRECEDENCE[stack[-1][-1]]):
                    output.append(stack.pop())
                stack.append(op_token)
            elif value_op == ")":
                while stack and stack[-1][-1] != "(":
                    output.append(stack.pop())
                stack.pop()
        elif token_type == "EOF":
            break

    while stack:
        output.append(stack.pop())

    return output
