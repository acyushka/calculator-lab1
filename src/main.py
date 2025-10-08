from src.tokenizer import tokenize, CalcError
from src.converter import convert_to_rpn
from src.rpn_calculate import calculate_rpn
from src.validators import validate_brackets, validate_expr_struct, validate_two_operators


def main() -> None:
    """
    Точка входа в приложение
    :return: Данная функция ничего не возвращает
    """
    while True:
        try:
            expression: str = input("Введите выражение: ")

            # Выхода из калькулятора
            if expression.lower() == "exit":
                break

            # Токенизация
            tokens = tokenize(expression)

            # Этап валидации токенов
            validate_expr_struct(tokens)  # валидация операторов на концах
            validate_two_operators(tokens)  # валидация 2 чисел подряд
            validate_brackets(tokens)  # валидация скобок

            # Перевод в обратную польскую нотацию
            rpn_expression = convert_to_rpn(tokens)

            # Подсчет RPN выражения
            result = calculate_rpn(rpn_expression)

            # Вывод в консоль
            print("Результат: ", result)

        except CalcError as err:
            print(f"Ошибка: {err}")
        except Exception as err:
            print(f"Неопознанная ошибка: {err}")


if __name__ == "__main__":
    main()
