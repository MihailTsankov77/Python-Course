

class Ticker:

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self.counter = 0

    def tick(self):
        self.counter += 1


class Wrapper:
    def __init__(self, wrapper_target):
        self.wrapper_target = wrapper_target

    def __getattr__(self, name):
        return getattr(self.wrapper_target, name)


class Potion:

    def enchant(_, target):

        wrapped_target = Wrapper(target)

        class EnchantedTarget:
            ticker = Ticker()

            def __init__(self, target):
                self.target = target

            def __getattribute__(self, name):
                if EnchantedTarget.ticker.counter < 2:
                    Potion.effect(wrapped_target)
                    return getattr(wrapped_target, name)

                return getattr(target, name)

        return EnchantedTarget(target)

    @staticmethod
    def effect(target):

        target.x *= 2


class TestClass:
    x = 4

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)


# use face target for the effect

potion = Potion()

narco = Ticker()

test = TestClass()

test = potion.enchant(test)

print(test.x)

narco.tick()
print(test.x)

narco.tick()
print(test.x)
