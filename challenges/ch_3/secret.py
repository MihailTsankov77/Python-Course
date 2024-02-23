

class path_clue:

    class clue_1:
        def clue_5():
            return "bob"

        def A(a):
            if a % 2 == 0:
                return a**2

            return 1

        class clue_4:
            @staticmethod
            def C(a, b):
                ...

    class clue_2:
        clue_23 = "bob"

        class clue_3:
            def b(left=1, right=2):
                return left + right

    def F():
        ...


def fn():
    raise TypeError('Опаааааа, тука има нещо нередно.')


def fn2():
    raise BaseException('Опаааааа, тука има нещо нередно.')


def baba(a):
    if a % 2 == 0:
        return a**2

    return 0


setattr(path_clue, "1", fn)
setattr(path_clue.clue_2.clue_3, "2", fn2)
setattr(path_clue.clue_2.clue_3, "A", baba)
