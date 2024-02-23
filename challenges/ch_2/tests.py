from witch import *

LogicMixin = logic_mixin_factory(20, 'mass', 'wood', 'material', 'float')


class Woman(LogicMixin):
    def __init__(self):
        self.mass = 201
        self.materi1al = 'wood'

    def float1(self):
        print('I am floating')
        return True

    def burn(self):
        return True


woman = Woman()

print(woman.is_a_witch())
