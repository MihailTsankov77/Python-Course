from typing import Any


class Ticker:
    def __init__(self):
        self.ticker = 0

    def tick(self):
        self.ticker += 1


class TestClass:
    x = 0

    def __getattribute__(self, name):
        if name == "x":
            print(narco.ticker)
            return object.__getattribute__(self, name)


# use face target for the effect

narco = Ticker()

test = TestClass()

TestClass.__Ticker__ = narco


# test.x

# narco.tick()
# test.x

# narco.tick()
# test.x


class TestTarget:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


teas = TestTarget(1, 2, 3)

teas.x = 2

print(teas == TestTarget(4, 2, 3))
