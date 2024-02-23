from witchcraft import *

import unittest

grow = {'grow': lambda _: setattr(_, 'size', _.size * 2)}
heal = {'heal': lambda _: setattr(_, 'health', _.health + 10)}
strengthen = {'strengthen': lambda _: setattr(_, 'strength', _.strength + 20)}
fly = {'fly': lambda _: setattr(_, 'fly', True)}
invisible = {'invisible': lambda _: setattr(_, 'invisible', True)}
glow = {'glow': lambda _: setattr(_, 'glow', _.glow * 3)}
armor = {'armor': lambda _: setattr(_, 'armor', _.armor + 5)}
speed = {'speed': lambda _: setattr(_, 'speed', _.speed * 2)}
power = {'power': lambda _: setattr(_, 'power', 200)}

TRANSCENDED = 'Potion is now part of something bigger than itself.'
DEPLETED_P = 'Potion is depleted.'
DEPLETED_E = 'Effect is depleted.'


class Target:
    def __init__(self, **kwargs):
        for prop, val in kwargs.items():
            setattr(self, prop, val)


class PotionTest(unittest.TestCase):
    def test_use_potion_effect_once(self):
        grow_potion = Potion(grow, 1)
        target = Target(size=10)

        grow_potion.grow(target)

        self.assertEqual(20, target.size)
        with self.assertRaises(TypeError) as e:
            grow_potion.grow(target)
        self.assertEqual(DEPLETED_E, str(e.exception))

    def test_combined_potion_has_all_effects(self):
        grow_heal_potion = Potion(grow | heal, 1)
        fly_invis_potion = Potion(fly | invisible, 1)

        all_potion = grow_heal_potion + fly_invis_potion

        self.assertTrue('grow' in all_potion.effects)
        self.assertTrue('heal' in all_potion.effects)
        self.assertTrue('invisible' in all_potion.effects)
        self.assertTrue('fly' in all_potion.effects)

    def test_combined_potion_has_increased_intensity(self):
        triple_grow_potion = Potion(grow, 1) + Potion(grow, 1) + Potion(grow, 1)
        target = Target(size=8)

        triple_grow_potion.grow(target)
        self.assertEqual(64, target.size)

    def test_combined_potion_has_longer_duration(self):
        heal_potion = Potion(heal, 10)
        grow_potion = Potion(grow, 5)
        fly_potion = Potion(fly, 7)

        triple_potion = heal_potion + grow_potion + fly_potion

        self.assertEqual(10, triple_potion.duration)

    def test_potented_potion_has_increased_intensity(self):
        heal_grow_potion = Potion(heal | grow, 1)
        potented_potion = heal_grow_potion * 5
        target = Target(size=1, health=19)

        potented_potion.heal(target)
        potented_potion.grow(target)
        self.assertEqual(69, target.health)
        self.assertEqual(32, target.size)

    def test_diluted_potion_has_decreased_intensity_rounded_half_down(self):
        heal_2_grow_4_potion = Potion(heal, 1) * 2 + Potion(grow, 1) * 4
        diluted_grow_potion = heal_2_grow_4_potion * 0.625
        target = Target(size=25, health=10)

        diluted_grow_potion.grow(target)
        diluted_grow_potion.heal(target)
        self.assertEqual(100, target.size)
        self.assertEqual(20, target.health)

    def test_diluted_potion_has_decreased_intensity_rounded_half_up(self):
        triple_heal_potion = Potion(heal, 1) * 3
        diluted_potion = triple_heal_potion * 0.6
        target = Target(health=10)

        diluted_potion.heal(target)
        self.assertEqual(30, target.health)

    def test_diluted_potion_with_zero_intensity(self):
        fly_potion = Potion(fly, 1) * 0
        target = Target(fly=False)

        self.assertTrue('fly' in fly_potion.effects)
        fly_potion.fly(target)
        self.assertFalse(target.fly)

    def test_purify_with_potion_that_has_more_effects(self):
        heal_grow_potion = Potion(heal | grow, 1)
        heal_fly_potion = Potion(heal | fly, 1)

        with self.assertRaises(TypeError):
            heal_grow_potion - heal_fly_potion

    def test_purify_potion_decreases_intensities_removes_non_positive_effects(self):
        heal_grow_power_armor_speed_potion = (Potion(armor, 1) * 3 + Potion(grow, 1) * 4
                                              + Potion(heal, 1) * 3 + Potion(power, 1) + Potion(speed, 8) * 2)
        heal_grow_power_armor_potion = (Potion(grow, 1) * 2 + Potion(heal, 1) * 3
                                        + Potion(power, 1) * 3 + Potion(armor, 1) * 0)

        grow_armor_speed_potion = heal_grow_power_armor_speed_potion - heal_grow_power_armor_potion

        with self.assertRaises(AttributeError):
            grow_armor_speed_potion.heal
        with self.assertRaises(AttributeError):
            grow_armor_speed_potion.power

        target = Target(armor=10, size=20, speed=10)
        grow_armor_speed_potion.grow(target)
        grow_armor_speed_potion.armor(target)
        grow_armor_speed_potion.speed(target)

        self.assertEqual(80, target.size)
        self.assertEqual(25, target.armor)
        self.assertEqual(40, target.speed)

    def test_purify_potion_that_has_used_effect(self):
        heal_grow_potion = Potion(heal | grow, 1) * 3
        heal_grow_potion.grow(Target(size=0))

        grow_potion = Potion(grow, 2) * 2

        heal_potion = heal_grow_potion - grow_potion

        with self.assertRaises(AttributeError):
            heal_potion.grow

        target = Target(health=60)
        heal_potion.heal(target)
        self.assertEqual(90, target.health)

    def test_purify_potion_with_one_that_has_used_effects(self):
        power_speed_potion = Potion(power, 1) * 3 + Potion(speed, 1)
        speed_potion = Potion(speed, 1)

        speed_potion.speed(Target(speed=0))

        purified_power_speed_potion = power_speed_potion - speed_potion

        target = Target(power=10, speed=40)
        purified_power_speed_potion.power(target)
        purified_power_speed_potion.speed(target)

        self.assertEqual(200, target.power)
        self.assertEqual(80, target.speed)

    @unittest.skip
    def test_purify_potion_undefined_case_vol_1(self):
        heal_grow_potion = Potion(heal, 1) * 2 + Potion(grow, 2) * 0
        used_grow_potion = Potion(grow, 1)
        used_grow_potion.grow(Target())

        target = Target(size=10)
        (heal_grow_potion - used_grow_potion).grow(target)
        self.assertEqual(10, target.size)

    @unittest.skip
    def test_purify_potion_undefined_case_vol_2(self):
        heal_fly_potion = Potion(heal | fly, 2) * 3
        heal_fly_potion.heal(Target())
        fly_potion = Potion(fly, 2) * 10

        with self.assertRaises(AttributeError):
            (heal_fly_potion - fly_potion).heal(Target())

    def test_purify_potion_removes_all_effects(self):
        heal_potion = Potion(heal, 1)
        double_heal_potion = Potion(heal, 2) * 2

        empty_potion = heal_potion - double_heal_potion

        with self.assertRaises(AttributeError):
            empty_potion.heal(Target())

    def test_divide_potion_has_divided_intensity(self):
        fly_heal_grow_strengthen = (Potion(fly, 1) * 4 + Potion(heal, 1) * 10 +
                                    Potion(grow, 1) * 5 + Potion(strengthen, 1) * 15)
        fly_heal_grow_strengthen.fly(Target())
        one_fourth_1, one_fourth_2, one_fourth_3, one_fourth_4 = fly_heal_grow_strengthen / 4

        with self.assertRaises(AttributeError):
            one_fourth_2.fly(Target())
        target1 = Target(health=0)
        one_fourth_1.heal(target1)
        self.assertEqual(20, target1.health)

        target2 = Target(size=10, strength=20, health=10)
        one_fourth_2.heal(target2)
        one_fourth_2.grow(target2)
        one_fourth_2.strengthen(target2)
        self.assertEqual(30, target2.health)
        self.assertEqual(20, target2.size)
        self.assertEqual(100, target2.strength)

        target3 = Target(size=20)
        one_fourth_3.grow(target3)
        self.assertEqual(40, target3.size)

        target4 = Target(strength=100)
        one_fourth_4.strengthen(target4)
        self.assertEqual(180, target4.strength)

    def test_potion_transcends_after_sum(self):
        heal_potion = Potion(heal, 1)
        power_grow_potion = Potion(power | grow, 3)
        fly_potion = Potion(fly, 1)

        heal_potion + power_grow_potion + fly_potion

        with self.assertRaises(TypeError) as e:
            heal_potion.heal(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

        with self.assertRaises(TypeError) as e:
            power_grow_potion.power(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

        with self.assertRaises(TypeError) as e:
            power_grow_potion.grow(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

        with self.assertRaises(TypeError) as e:
            fly_potion.fly(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

    def test_transcends_after_potention(self):
        power_grow_potion = Potion(power | grow, 1)
        power_grow_potion * 69

        with self.assertRaises(TypeError) as e:
            power_grow_potion.grow(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

        with self.assertRaises(TypeError) as e:
            power_grow_potion.power(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

    def test_transcends_after_dilution(self):
        speed_potion = Potion(speed, 0)
        speed_potion * 0.1

        with self.assertRaises(TypeError) as e:
            speed_potion.speed(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

    def test_transcends_after_purification(self):
        heal_grow_potion = Potion(heal | grow, 1)
        grow_potion = Potion(grow, 1)

        heal_grow_potion - grow_potion

        with self.assertRaises(TypeError) as e:
            heal_grow_potion.heal(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

        with self.assertRaises(TypeError) as e:
            heal_grow_potion.grow(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

        with self.assertRaises(TypeError) as e:
            grow_potion.grow(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

    def test_transcends_after_division(self):
        power_armor_potion = Potion(power | armor, 1)
        power_armor_potion / 10

        with self.assertRaises(TypeError) as e:
            power_armor_potion.power(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

        with self.assertRaises(TypeError) as e:
            power_armor_potion.armor(Target())
        self.assertEqual(TRANSCENDED, str(e.exception))

    def test_combine_potions(self):
        heal_grow_speed_glow = (Potion(heal, 1) * 2 + Potion(grow, 1) * 5
                                + Potion(speed, 1) + Potion(glow, 1))
        heal_grow_speed_glow.heal(Target(health=0))
        heal_grow_speed_glow.glow(Target(glow=0))

        heal_speed_grow_glow_armor = (Potion(heal, 1) * 3 + Potion(speed, 1) * 2
                                      + Potion(grow, 1) * 2 + Potion(glow, 2) * 2 + Potion(armor, 2) * 0)
        heal_speed_grow_glow_armor.speed(Target(speed=0))
        heal_speed_grow_glow_armor.glow(Target(glow=0))

        combined = heal_grow_speed_glow + heal_speed_grow_glow_armor
        with self.assertRaises(AttributeError):
            combined.glow

        target = Target(health=10, size=1, speed=10, armor=20)

        combined.heal(target)
        combined.grow(target)
        combined.speed(target)
        combined.armor(target)

        self.assertEqual(40, target.health)
        self.assertEqual(128, target.size)
        self.assertEqual(20, target.speed)
        self.assertEqual(20, target.armor)

    def test_potent_potion(self):
        heal_grow_speed = Potion(heal | grow | speed, 1)
        heal_grow_speed.heal(Target(health=0))

        eleventh = heal_grow_speed * 11

        with self.assertRaises(AttributeError):
            eleventh.heal(Target(health=10))

        target = Target(size=1, speed=1)
        eleventh.speed(target)
        eleventh.grow(target)
        self.assertEqual((2048, 2048), (target.speed, target.size))

    def test_comparing_potions(self):
        grow_potion = Potion(grow, 1)
        double_grow_potion = Potion(grow, 1) * 2
        invisible_fly_potion = Potion(invisible | fly, 1)

        self.assertTrue(grow_potion == grow_potion)
        self.assertFalse(grow_potion < grow_potion)
        self.assertTrue(double_grow_potion > grow_potion)
        self.assertTrue(invisible_fly_potion > grow_potion)
        self.assertFalse(double_grow_potion < invisible_fly_potion)
        self.assertFalse(double_grow_potion > invisible_fly_potion)

    def test_compare_potions_with_used_effects(self):
        grow_heal_speed_potion = Potion(grow, 1) * 0 + Potion(heal, 1) * 2 + Potion(speed, 2)
        used_grow_heal_speed_potion = Potion(grow | speed, 4) + Potion(heal, 2) * 2
        used_grow_heal_speed_potion.grow(Target(size=0))

        self.assertTrue(grow_heal_speed_potion == used_grow_heal_speed_potion)

        grow_heal_speed_potion -= Potion(grow, 1)

        self.assertFalse(grow_heal_speed_potion == used_grow_heal_speed_potion)

    def test_apply_potion_sorted_by_mass(self):
        grow_potion = Potion(grow | {'little_grow': lambda _: setattr(_, 'size', _.size + 20),
                                     'shr': lambda _: setattr(_, 'size', _.size - 10)}, 1)
        target = Target(size=10)
        ГоспожатаПоХимия().apply(target, grow_potion)

        self.assertEqual(50, target.size)

    def test_deplete_potion_after_appy(self):
        heal_potion = Potion(heal, 1)
        target = Target(health=90)
        ГоспожатаПоХимия().apply(target, heal_potion)

        with self.assertRaises(TypeError) as e:
            heal_potion.heal(target)
        self.assertEqual(100, target.health)
        self.assertEqual(DEPLETED_P, str(e.exception))

        with self.assertRaises(TypeError) as e:
            heal_potion + Potion({}, 1)
        self.assertEqual(DEPLETED_P, str(e.exception))

        with self.assertRaises(TypeError) as e:
            heal_potion - Potion({}, 1)
        self.assertEqual(DEPLETED_P, str(e.exception))

        with self.assertRaises(TypeError) as e:
            heal_potion * Potion({}, 1)
        self.assertEqual(DEPLETED_P, str(e.exception))

        with self.assertRaises(TypeError) as e:
            heal_potion / 2
        self.assertEqual(DEPLETED_P, str(e.exception))

        with self.assertRaises(TypeError) as e:
            heal_potion == Potion({}, 1)
        self.assertEqual(DEPLETED_P, str(e.exception))

        with self.assertRaises(TypeError) as e:
            heal_potion < Potion({}, 1)
        self.assertEqual(DEPLETED_P, str(e.exception))

        with self.assertRaises(TypeError) as e:
            ГоспожатаПоХимия().apply(Target(), heal_potion)
        self.assertEqual(DEPLETED_P, str(e.exception))

    def test_dimitrichka_with_zero_duration_potion(self):
        grow_potion = Potion(grow, 0)
        target = Target(size=10)
        димитричка = ГоспожатаПоХимия()
        димитричка.apply(target, grow_potion)
        self.assertEqual(10, target.size)

    def test_dimitrichka_with_used_effects(self):
        heal_grow_power_potion = Potion(heal | grow | power, 1)
        heal_grow_power_potion.power(Target())

        pastichka = ГоспожатаПоХимия()
        target = Target(health=10, size=10, power=10)
        pastichka.apply(target, heal_grow_power_potion)

        self.assertEqual(20, target.health)
        self.assertEqual(20, target.size)
        self.assertEqual(10, target.power)

    def test_dimitrichka_with_one_poor_addict(self):
        heal_invisible_fly_potion = Potion(heal, 2) * 3 + Potion(fly | invisible, 3)
        target = Target(health=30, fly=False, invisible=False)
        пастичка = ГоспожатаПоХимия()

        пастичка.apply(target, heal_invisible_fly_potion)
        self.assertEqual(60, target.health)
        self.assertTrue(target.fly)
        self.assertTrue(target.invisible)

        пастичка.tick()
        self.assertEqual(60, target.health)
        self.assertTrue(target.fly)
        self.assertTrue(target.invisible)

        пастичка.tick()
        self.assertEqual(60, target.health)
        self.assertTrue(target.fly)
        self.assertTrue(target.invisible)

        пастичка.tick()
        self.assertEqual(30, target.health)
        self.assertFalse(target.fly)
        self.assertFalse(target.invisible)

    def test_dimitrichka_with_strong_drugs(self):
        power_potion = Potion(power, 2)
        target = Target()
        power_dimitrichka = ГоспожатаПоХимия()

        power_dimitrichka.apply(target, power_potion)
        self.assertEqual(200, target.power)

        power_dimitrichka.tick()
        power_dimitrichka.tick()
        self.assertFalse(hasattr(target, 'power'))

    def test_dimitrichka_with_one_rich_addict(self):
        heal_strengthen_potion = Potion(heal, 2) * 2 + Potion(strengthen, 1)
        grow_potion = Potion(grow, 2)
        target = Target(size=10, health=10, strength=10)
        narco = ГоспожатаПоХимия()

        narco.apply(target, heal_strengthen_potion)
        narco.tick()

        narco.apply(target, grow_potion)
        self.assertEqual(20, target.size)
        self.assertEqual(30, target.health)
        self.assertEqual(30, target.strength)

        narco.tick()
        self.assertEqual(20, target.size)
        self.assertEqual(10, target.health)
        self.assertEqual(10, target.strength)

        narco.tick()
        self.assertEqual(10, target.size)
        self.assertEqual(10, target.health)
        self.assertEqual(10, target.strength)

    def test_dimitrichka_with_potion_that_add_attributes(self):
        power_potion = Potion(power, 5)
        target = Target()
        narco = ГоспожатаПоХимия()

        narco.apply(target, power_potion)
        self.assertEqual(200, target.power)

        narco.tick()
        narco.tick()
        narco.tick()
        narco.tick()
        narco.tick()

        self.assertFalse(hasattr(target, 'power'))

    def test_dimitrichka_with_potion_that_removes_attributes(self):
        fmi_potion = Potion({'insomnia': lambda _: delattr(_, 'sleep')}, 3)
        student = Target(sleep='lovely')

        narco = ГоспожатаПоХимия()
        narco.apply(student, fmi_potion)
        self.assertFalse(hasattr(student, 'sleep'))
        narco.tick()
        narco.tick()
        narco.tick()
        self.assertTrue('lovely', student.sleep)