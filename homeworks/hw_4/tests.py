from witchcraft import *
import unittest


class TestTarget:
    opa = "opa"

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.size == other.size


def get_teleport_potion():
    def teleport(target):
        target.x *= 100
        target.y *= 100

    effects = {'teleport': teleport}

    teleport_potion = Potion(effects, duration=3)

    return teleport_potion


def get_grow_potion():
    effects = {'grow': lambda target: setattr(
        target, 'size', target.size*2)}

    grow_potion = Potion(effects, duration=2)

    return grow_potion


class WitchCraftTest(unittest.TestCase):

    def test_basic_potion_with_one_effect(self):
        target = TestTarget(0, 0, 1)
        potion = get_grow_potion()
        potion.grow(target)

        self.assertEqual(target.size, 2)

    def test_basic_potion_with_two_effects(self):
        effects = {'grow': lambda target: setattr(target, 'size', target.size*2),
                   'moveX': lambda target: setattr(target, 'x', 1)}

        potion = Potion(effects, 1)

        target = TestTarget(0, 0, 1)
        potion.grow(target)
        potion.moveX(target)

        self.assertEqual(2, target.size)
        self.assertEqual(1, target.x)

    def test_potion_depleted_effect(self):
        target = TestTarget(0, 0, 1)
        potion = get_grow_potion()

        potion.grow(target)

        with self.assertRaises(TypeError) as context:
            potion.grow(target)

        self.assertTrue("Effect is depleted." in str(context.exception))

    def test_potion_with_two_effects_depleted_effect(self):
        effects = {'grow': lambda target: setattr(target, 'size', target.size*2),
                   'moveX': lambda target: setattr(target, 'x', 10)}

        potion = Potion(effects, 1)

        target = TestTarget(0, 0, 1)

        potion.grow(target)

        with self.assertRaises(TypeError) as context:
            potion.grow(target)

        potion.moveX(target)

        self.assertTrue("Effect is depleted." in str(context.exception))
        self.assertEqual(10, target.x)
        self.assertEqual(2, target.size)

    def test_potion_effect_duration(self):
        narco = ГоспожатаПоХимия()
        grow_potion = get_grow_potion()

        target = TestTarget(0, 0, 5)

        grow_potion.grow(target)

        narco.tick()
        narco.tick()
        narco.tick()

        self.assertEqual(10, target.size)

    def test_teleport_potion(self):
        teleport_potion = get_teleport_potion()

        target = TestTarget(1, 1, 0)

        teleport_potion.teleport(target)

        self.assertEqual(TestTarget(100, 100, 0), target)

    def test_combined_potions_basic(self):
        teleport_potion = get_teleport_potion()
        grow_potion = get_grow_potion()

        combined_potion = teleport_potion + grow_potion

        target = TestTarget(1, 1, 1)

        combined_potion.teleport(target)
        combined_potion.grow(target)

        self.assertEqual(TestTarget(100, 100, 2), target)

    def test_combined_potions_depleted_effect(self):
        combined_potion = get_teleport_potion() + get_grow_potion()

        target = TestTarget(1, 1, 1)

        combined_potion.teleport(target)
        combined_potion.grow(target)

        with self.assertRaises(TypeError) as context:
            combined_potion.grow(target)

        self.assertTrue("Effect is depleted." in str(context.exception))
        self.assertEqual(TestTarget(100, 100, 2), target)

    def test_combined_potions_effect_duration(self):
        combined_potion = get_teleport_potion() + get_grow_potion()

        self.assertEqual(3, combined_potion.duration)

    def test_combined_potions_potion_already_used(self):
        grow_potion = get_grow_potion()
        teleport_potion = get_teleport_potion()

        combined_potion = grow_potion + teleport_potion

        with self.assertRaises(TypeError) as context:
            _ = combined_potion + teleport_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_combined_potions_potion_already_used_reverse(self):
        grow_potion = get_grow_potion()
        teleport_potion = get_teleport_potion()

        combined_potion = grow_potion + teleport_potion

        with self.assertRaises(TypeError) as context:
            _ = teleport_potion + combined_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_combined_potions_intensity(self):
        combined_potion = get_grow_potion() + get_teleport_potion() + get_grow_potion()

        target = TestTarget(1, 1, 2)

        combined_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 8), target)

    def test_combined_potions_intensity_depleted_effect(self):
        combined_potion = get_grow_potion() + get_teleport_potion()

        target = TestTarget(1, 1, 2)

        combined_potion.grow(target)

        with self.assertRaises(TypeError) as context:
            combined_potion.grow(target)

        self.assertTrue("Effect is depleted." in str(context.exception))
        self.assertEqual(TestTarget(1, 1, 4), target)

    def test_combined_potions_intensity_2(self):
        teleport_and_grow_potion = get_teleport_potion() + get_grow_potion()

        combined_potion = teleport_and_grow_potion + get_grow_potion()

        target = TestTarget(1, 1, 2)

        combined_potion.grow(target)
        combined_potion.teleport(target)

        self.assertEqual(TestTarget(100, 100, 8), target)

    def test_super_teleport(self):
        teleport_potion = get_teleport_potion() * 3

        target = TestTarget(1, 1, 1)

        teleport_potion.teleport(target)

        self.assertEqual(TestTarget(1000000, 100 ** 3, 1), target)

    def test_jaeger_bomb(self):
        triple_grow_potion = get_grow_potion() * 3

        jaeger_bomb_potion = triple_grow_potion * 0.33

        target = TestTarget(1, 1, 1)

        jaeger_bomb_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 2), target)

    def test_tears(self):
        triple_grow_potion = get_grow_potion() * 3

        tears_potion = triple_grow_potion * 0.5

        target = TestTarget(1, 1, 1)

        tears_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 2), target)

    def test_water(self):
        triple_grow_potion = get_grow_potion() * 3

        water_potion = triple_grow_potion * 0.75

        target = TestTarget(1, 1, 1)

        water_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 4), target)

    def test_potion_neg_already_used(self):
        grow_potion = get_grow_potion()
        triple_grow_potion = grow_potion * 3

        _ = triple_grow_potion * 0.5

        with self.assertRaises(TypeError) as context:
            _ = grow_potion * 0.3

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

        with self.assertRaises(TypeError) as context:
            _ = triple_grow_potion * 3

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_potion_neg_already_used_other_test(self):
        grow_potion = get_grow_potion()
        _ = grow_potion * 3

        with self.assertRaises(TypeError) as context:
            grow_potion.grow(TestTarget(1, 1, 1))

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_zero_intensity(self):
        no_grow_potion = get_grow_potion() * 0

        target = TestTarget(1, 1, 1)

        no_grow_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 1), target)

    def test_zero_intensity_combine_1(self):
        no_grow_potion = get_grow_potion() * 0

        combined_potion = no_grow_potion + get_grow_potion()

        target = TestTarget(1, 1, 1)
        combined_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 2), target)

    def test_zero_intensity_combine_2(self):
        no_grow_potion = get_grow_potion() * 0

        combined_potion = no_grow_potion + get_teleport_potion()

        target = TestTarget(1, 1, 1)
        combined_potion.grow(target)
        combined_potion.teleport(target)

        self.assertEqual(TestTarget(100, 100, 1), target)

    def test_purify_potion_basic(self):
        grow_teleport_potion = get_grow_potion() + get_teleport_potion()*2

        purified_potion = grow_teleport_potion - get_grow_potion()

        target = TestTarget(1, 1, 1)

        purified_potion.teleport(target)
        self.assertEqual(TestTarget(10000, 10000, 1), target)

        with self.assertRaises(AttributeError):
            purified_potion.grow(target)

    def test_purify_potion_intensity_effect(self):
        triple_grow_potion = get_grow_potion() * 3

        purified_potion = triple_grow_potion - get_grow_potion()

        target = TestTarget(1, 1, 1)

        purified_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 4), target)

    def test_purify_potion_more_effect(self):
        with self.assertRaises(TypeError):
            _ = get_grow_potion() - get_teleport_potion()

    def test_purify_potion_more_effect_2(self):
        triple_grow_potion = get_grow_potion() * 3
        double_teleport_potion = get_teleport_potion() * 2 + get_grow_potion()

        purified_potion = double_teleport_potion - triple_grow_potion

        target = TestTarget(1, 1, 1)

        with self.assertRaises(AttributeError):
            purified_potion.grow(target)

    def test_purify_potion_duration(self):
        combined_potion = get_grow_potion() + get_teleport_potion()

        purified_potion = combined_potion - get_teleport_potion()

        self.assertEqual(3, purified_potion.duration)

    def test_split_potion_basic(self):
        triple_grow_potion = get_grow_potion() * 3

        split_potion, _, _ = triple_grow_potion / 3

        target = TestTarget(1, 1, 1)

        split_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 2), target)

    def test_split_potion_rounding(self):
        triple_grow_potion = get_grow_potion() * 3

        split_potion, _ = triple_grow_potion / 2

        target = TestTarget(1, 1, 1)

        split_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 2), target)

    def test_split_potion_rounding_2(self):
        triple_grow_potion = get_grow_potion() * 5

        split_potion, _, _ = triple_grow_potion / 3

        target = TestTarget(1, 1, 1)

        split_potion.grow(target)

        self.assertEqual(TestTarget(1, 1, 4), target)

    def test_split_potion_rounding_3(self):
        triple_grow_potion = get_grow_potion() * 3

        split_potion_1, split_potion_2, split_potion_3 = triple_grow_potion / 3

        target = TestTarget(1, 1, 1)

        split_potion_1.grow(target)
        split_potion_2.grow(target)
        split_potion_3.grow(target)

        self.assertEqual(TestTarget(1, 1, 8), target)

    def test_split_potion_rounding_4(self):
        triple_grow_potion = get_grow_potion() * 3

        _, _, _ = triple_grow_potion / 3

        with self.assertRaises(TypeError) as context:
            triple_grow_potion = triple_grow_potion * 3

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_potion_equality_basic(self):
        self.assertTrue(get_grow_potion() == get_grow_potion())

    def test_potion_equality_basic_2(self):
        self.assertFalse(get_grow_potion() == (get_grow_potion() * 2))

    def test_potion_equality(self):
        combined_potion = get_grow_potion() + get_teleport_potion()
        self.assertFalse(combined_potion == get_grow_potion())

    def test_potion_equal_is_used_1(self):
        grow_potion = get_grow_potion()
        combined_potion = grow_potion + get_teleport_potion()

        with self.assertRaises(TypeError) as context:
            grow_potion == combined_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))
    
    def test_potion_equal_is_used_2(self):
        grow_potion = get_grow_potion()
        combined_potion = grow_potion + get_teleport_potion()

        with self.assertRaises(TypeError) as context:
            combined_potion == grow_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))
        
    def test_potion_equal_complex(self):
        double_grow_potion = get_grow_potion() * 2
        combined_potion = double_grow_potion + get_teleport_potion()

        self.assertFalse(combined_potion == (get_grow_potion() * 3))

        combined_potion = combined_potion - get_grow_potion()

        self.assertTrue(combined_potion == (get_grow_potion() + get_teleport_potion()))

        with self.assertRaises(TypeError) as context:
            combined_potion == double_grow_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))
    
    def test_potion_bigger_basic(self):
        self.assertFalse(get_grow_potion() > get_teleport_potion())

    def test_potion_bigger_basic_2(self):
        self.assertTrue((get_grow_potion()*2) > get_grow_potion())

    def test_potion_bigger(self):
        combined_potion = get_grow_potion() + get_teleport_potion()

        self.assertFalse((get_grow_potion()*2) > combined_potion)

    def test_potion_bigger_is_used_1(self):
        grow_potion = get_grow_potion()
        combined_potion = grow_potion + get_teleport_potion()

        with self.assertRaises(TypeError) as context:
            grow_potion > combined_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))
        
    def test_potion_bigger_is_used_2(self):
        grow_potion = get_grow_potion()
        combined_potion = grow_potion + get_teleport_potion()

        with self.assertRaises(TypeError) as context:
            combined_potion > grow_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_potion_bigger_2(self):
        combined_potion = get_grow_potion()*3 + get_teleport_potion()

        self.assertTrue(combined_potion > (get_grow_potion()*2))

    def test_potion_lesser_basic(self):
        self.assertFalse(get_grow_potion() < get_teleport_potion())

    def test_potion_lesser_basic_2(self):
        self.assertFalse((get_grow_potion() * 2) < get_grow_potion())

    def test_potion_lesser_basic_3(self):
        self.assertTrue(get_grow_potion() < (get_grow_potion() * 2))

    def test_potion_lesser(self):
        combined_potion = get_grow_potion() + get_teleport_potion()

        self.assertFalse((get_grow_potion() * 2) < combined_potion)

    def test_potion_lesser_is_used_1(self):
        grow_potion = get_grow_potion()
        combined_potion = grow_potion + get_teleport_potion()

        with self.assertRaises(TypeError) as context:
            grow_potion < combined_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))
        
    def test_potion_lesser_is_used_2(self):
        grow_potion = get_grow_potion()
        combined_potion = grow_potion + get_teleport_potion()

        with self.assertRaises(TypeError) as context:
            combined_potion< grow_potion

        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_potion_lesser_2(self):
        combined_potion = get_grow_potion() + get_teleport_potion()

        self.assertTrue(combined_potion < (get_grow_potion() * 3))

    def test_narco_basic(self):
        target = TestTarget(1, 1, 1)
        ГоспожатаПоХимия().apply(target, get_grow_potion())

        self.assertEqual(TestTarget(1, 1, 2), target)

    def test_narco_basic_2(self):
        target = TestTarget(1, 1, 1)
        ГоспожатаПоХимия().apply(target, get_grow_potion() * 2)

        self.assertEqual(TestTarget(1, 1, 4), target)

    def test_narco_basic_3(self):
        target = TestTarget(1, 1, 1)
        ГоспожатаПоХимия().apply(target, get_grow_potion() +
                                 get_teleport_potion() + get_grow_potion())

        self.assertEqual(TestTarget(100, 100, 4), target)

    def test_narco_potion_depleted(self):
        grow_potion = get_grow_potion()
        target = TestTarget(1, 1, 1)

        ГоспожатаПоХимия().apply(target, grow_potion)

        with self.assertRaises(TypeError) as context:
            ГоспожатаПоХимия().apply(target, grow_potion)

        self.assertTrue("Potion is depleted." in str(context.exception))
        self.assertEqual(TestTarget(1, 1, 2), target)

    def test_narco_potion_depleted_2(self):
        grow_potion = get_grow_potion() * 2
        target = TestTarget(1, 1, 1)

        ГоспожатаПоХимия().apply(target, grow_potion)

        with self.assertRaises(TypeError) as context_1:
            _ = grow_potion * 2

        with self.assertRaises(TypeError) as context_2:
            _ = grow_potion / 2

        with self.assertRaises(TypeError) as context_3:
            _ = grow_potion + get_grow_potion()

        self.assertTrue("Potion is depleted." in str(context_1.exception))
        self.assertTrue("Potion is depleted." in str(context_2.exception))
        self.assertTrue("Potion is depleted." in str(context_3.exception))
        self.assertEqual(TestTarget(1, 1, 4), target)

    def test_narco_potion_depleted_3(self):
        combined_potion = get_grow_potion() + get_teleport_potion()

        target = TestTarget(1, 1, 1)
        combined_potion.grow(target)

        target_2 = TestTarget(1, 1, 1)
        ГоспожатаПоХимия().apply(target_2, combined_potion)

        with self.assertRaises(TypeError) as context:
            ГоспожатаПоХимия().apply(target_2, combined_potion)

        self.assertTrue("Potion is depleted." in str(context.exception))
        self.assertEqual(TestTarget(1, 1, 2), target)
        self.assertEqual(TestTarget(100, 100, 1), target_2)

    def test_narco_potion_dead(self):
        grow_potion = get_grow_potion()
        combined_potion = grow_potion + get_teleport_potion()

        target = TestTarget(1, 1, 1)
        with self.assertRaises(TypeError) as context:
            ГоспожатаПоХимия().apply(target, grow_potion)

        ГоспожатаПоХимия().apply(target, combined_potion)

        self.assertEqual(TestTarget(100, 100, 2), target)
        self.assertTrue(
            "Potion is now part of something bigger than itself." in str(context.exception))

    def test_narco_potion_order(self):
        effects = {'fast': lambda target: setattr(target, 'size', target.size - 10),
                   'grow': lambda target: setattr(target, 'size', target.size*2)}

        potion = Potion(effects, duration=2)

        target = TestTarget(1, 1, 100)

        ГоспожатаПоХимия().apply(target, potion)

        self.assertEqual(TestTarget(1, 1, 190), target)

    def test_narco_potion_duration(self):
        narco = ГоспожатаПоХимия()
        target = TestTarget(1, 1, 1)
        narco.apply(target, get_grow_potion())

        self.assertEqual(TestTarget(1, 1, 2), target)
        narco.tick()
        self.assertEqual(TestTarget(1, 1, 2), target)
        narco.tick()
        self.assertEqual(TestTarget(1, 1, 1), target)

    def test_narco_potion_duration_2(self):
        grow_potion = get_grow_potion()

        effects = {'grow': lambda target: setattr(
            target, 'size', target.size + 100)}
        longer_grow_potion = Potion(effects, duration=4)

        narco = ГоспожатаПоХимия()
        target = TestTarget(1, 1, 10)

        narco.apply(target, grow_potion)
        narco.apply(target, longer_grow_potion)

        self.assertEqual(TestTarget(1, 1, 120), target)
        narco.tick()
        self.assertEqual(TestTarget(1, 1, 120), target)
        narco.tick()
        self.assertEqual(TestTarget(1, 1, 110), target)
        narco.tick()
        self.assertEqual(TestTarget(1, 1, 110), target)
        narco.tick()
        self.assertEqual(TestTarget(1, 1, 10), target)

    def test_narco_potion_duration_3(self):
        combined_potion = get_grow_potion() + get_teleport_potion()
        narco = ГоспожатаПоХимия()
        target = TestTarget(1, 1, 1)
        narco.apply(target, combined_potion)

        self.assertEqual(TestTarget(100, 100, 2), target)
        narco.tick()
        self.assertEqual(TestTarget(100, 100, 2), target)
        narco.tick()
        self.assertEqual(TestTarget(100, 100, 2), target)
        narco.tick()
        self.assertEqual(TestTarget(1, 1, 1), target)

    def test_narco_potion_duration_4(self):
        effects = {'fast': lambda target: setattr(target, 'opa', 'nono')}
        potion = Potion(effects, duration=2)
        narco = ГоспожатаПоХимия()
        target = TestTarget(1, 1, 1)
        narco.apply(target, potion)

        self.assertEqual('nono', target.opa)
        narco.tick()
        self.assertEqual('nono', target.opa)
        narco.tick()
        self.assertEqual('opa', target.opa)

    def test_narco_potion_duration_4(self):
        effects = {'fast': lambda target: setattr(target, 'opa', target.opa + 'nono')}
        potion = Potion(effects, duration=2)
        narco = ГоспожатаПоХимия()
        target = TestTarget(1, 1, 1)
        narco.apply(target, potion)

        self.assertEqual('opanono', target.opa)
        narco.tick()
        self.assertEqual('opanono', target.opa)
        narco.tick()
        self.assertEqual('opa', target.opa)
