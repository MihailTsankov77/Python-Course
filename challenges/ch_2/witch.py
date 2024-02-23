from collections import namedtuple


def logic_mixin_factory(mass, mass_attr_name, material, material_attr_name, float_method_name):

    Birthmark = namedtuple('Birthmark', ['key', 'value'], defaults=('', None))

    witch_birthmarks = [
        Birthmark(mass_attr_name, mass),
        Birthmark(material_attr_name, material),
        Birthmark(float_method_name)
    ]

    class LogicMixin:
        def is_a_witch(self):
            attributes = dir(self)
            for birthmark in witch_birthmarks:
                if birthmark.key not in attributes:
                    continue

                if (not birthmark.value and callable(getattr(self, birthmark.key))) or getattr(self, birthmark.key) == birthmark.value:
                    return "Burn her!"

            return "No, but it's a pity, cuz she looks like a witch!"

    return LogicMixin
