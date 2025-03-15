import math
from typing import Union


def sqrt(x: float) -> float:
    """
    setting sqrt function that calculate the square root of a given number
    :param x:
    :return: square root of x
    """
    if x < 0:
        raise ValueError
    return x ** 0.5


def avg(*args: float) -> float:
    """
    setting avg function that calculate the average of given args.
    It's not working well in eval, so I set it here separately
    :param args:
    :return: average of args
    """
    return sum(args)/len(args)


def custom_sum(*args: Union[int, float]) -> Union[int, float]:
    """
    sum in eval works only with 2 arguments, so I set this function to calculate the sum of args
    I did it with args based on the last Tirgul! thank you!
    :param args:
    :return: sum of args"""
    my_sum: float = 0
    for arg in args:
        my_sum += arg
    return my_sum


def sinus(x: float) -> float:
    x = math.radians(x)
    answer = math.sin(x)
    if math.isclose(answer, 0.0, abs_tol=1e-9):
        return 0.0
    return answer


def cosinus(x: float) -> float:
    x = math.radians(x)
    answer = math.cos(x)
    if math.isclose(answer, 0.0, abs_tol=1e-9):
        return 0.0
    return answer


def tangens(x: float) -> float:
    x = math.radians(x)
    answer = math.tan(x)
    if math.isclose(answer, 0.0, abs_tol=1e-9):
        return 0.0
    return answer
