import random
from inspect import getattr_static

import secret


fn = 'FN6MI0600150'


def catch_errors(fn):
    def wrapper(*args, **kwargs):
        try:
            check_result = fn(*args, **kwargs)
        except TypeError as error:
            return str(error) == 'Опаааааа, тука има нещо нередно.'
        except BaseException as error:
            return type(error) == BaseException

        return check_result
    return wrapper


@catch_errors
def call_no_args(method):
    method()


@catch_errors
def call_one_arg(method):
    value = (int)(random.random()*1000 + 666)

    even_value = value if value % 2 == 0 else value + 1
    odd_value = value if value % 2 == 1 else value + 1

    if method(even_value) != even_value**2:
        return False

    if method(odd_value) != 0:
        return False

    return True


@catch_errors
def call_two_args(method):
    return method(right='ba', left='ab') == 'abba'


def is_method_interesting(method):
    return True in call_no_args(method), call_one_arg(method), call_two_args(method)


def find_clue(object, interesting_methods):

    dictionary = dir(object)
    clues = []

    for item in dictionary:
        attr = getattr(object, item)

        if 'clue' not in item:
            if len(item) == 1 and callable(attr) and item in fn:
                if isinstance(getattr_static(object, item), staticmethod):
                    interesting_methods[item] = attr
                    continue

                if is_method_interesting(attr):
                    interesting_methods[item] = attr

            continue

        clues.append(getattr(object, item))

    for clue in clues:
        find_clue(clue, interesting_methods)


def methodify():
    interesting_methods = {}

    find_clue(secret, interesting_methods)

    return tuple(interesting_methods[key] for key in fn)
