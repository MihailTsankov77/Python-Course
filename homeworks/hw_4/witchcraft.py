from decimal import localcontext, Decimal, ROUND_HALF_DOWN
from functools import reduce
from copy import deepcopy

class Effect:
   
    @staticmethod
    def get_molecule_mass(name):
        return reduce(lambda a, b: a + ord(b), name, 0)

    def __init__(self, name, effect):
        self. is_depleted = False
        self.intensity = 1
        self.effect = effect
        self.molecule_mass = Effect.get_molecule_mass(name)

    def __call__(self, target):
        if self.is_depleted:
            raise TypeError("Effect is depleted.")

        for _ in range(self.intensity):
            self.effect(target)
        self.is_depleted = True
    
    def reapply(self, target):
        for _ in range(self.intensity):
            self.effect(target)


class Potion:

    def __init__(self, effects, duration):
        self.is_something_bigger = False
        self.is_depleted = False
        self.effects = {name: Effect(name, effect) for name, effect in effects.items()}
        self.duration = duration

    def __getattr__(self, name):
        if name in self.effects:
            if self.is_something_bigger:
                raise TypeError(
                    "Potion is now part of something bigger than itself.")

            if self.is_depleted:
                    raise TypeError("Potion is depleted.")

            return self.effects[name]

        raise AttributeError(f"No such effect: {name}")

    def get_check_for_deep_meaning_decorator(is_target):
        def check_for_deep_meaning_decorator(fun):
            def check_for_deep_meaning(self, target):
                if self.is_something_bigger or (is_target and target.is_something_bigger):
                    raise TypeError("Potion is now part of something bigger than itself.")
                  
                if self.is_depleted or (is_target and target.is_depleted):
                    raise TypeError("Potion is depleted.")
                
                return fun(self, target)
            return check_for_deep_meaning
        return check_for_deep_meaning_decorator

    def get_is_something_bigger_decorator(is_target):
        def is_something_bigger_decorator(fun):
            def is_something_bigger(self, target):
                self.is_something_bigger = True
                if is_target:
                    target.is_something_bigger = True
                return fun(self, target)
            return is_something_bigger
        return is_something_bigger_decorator

    @get_check_for_deep_meaning_decorator(True)
    @get_is_something_bigger_decorator(True)
    def __add__(self, other):
        new_duration = max(self.duration, other.duration)
        not_used_effects_potion_1 = filter(
            lambda item: not item[1].is_depleted,  self.effects.items())
        not_used_effects_potion_2 = filter(
            lambda item: not item[1].is_depleted,  other.effects.items())
        new_effects = dict(not_used_effects_potion_1)

        for key, effect in not_used_effects_potion_2:
            if key in new_effects:
                new_effects[key].intensity += effect.intensity
            else:
                new_effects[key] = effect

        new_potion = Potion({}, new_duration)
        new_potion.effects = new_effects

        return new_potion

    @staticmethod
    def round_half_down(num):
        with localcontext() as ctx:
            ctx.rounding = ROUND_HALF_DOWN
            return int(Decimal(num).to_integral_value())

    @get_check_for_deep_meaning_decorator(False)
    @get_is_something_bigger_decorator(False)
    def __mul__(self, number):
        new_effects = {}

        for key, effect in self.effects.items():
            if effect.is_depleted:
                continue

            new_effects[key] = Effect(key, effect.effect)
            new_effects[key].intensity = Potion.round_half_down(effect.intensity * number)

        new_potion = Potion({}, self.duration)
        new_potion.effects = new_effects

        return new_potion

    @get_check_for_deep_meaning_decorator(True)
    @get_is_something_bigger_decorator(True)
    def __sub__(self, target):
        new_effects = {}

        for key, effect in target.effects.items():
            if key not in self.effects:
                raise TypeError("Throwing Beans")

            if effect.is_depleted or self.effects[key].is_depleted:
                continue

            new_effect = Effect(key, effect.effect)
            new_effect.intensity = self.effects[key].intensity - effect.intensity
            if new_effect.intensity <= 0:
                continue
            new_effects[key] = new_effect

        for key, effect in self.effects.items():
            if key not in target.effects or (target.effects[key].is_depleted and not effect.is_depleted):
                new_effects[key] = effect
        
        new_potion = Potion({}, self.duration)
        new_potion.effects = new_effects
        return new_potion
    
    @get_check_for_deep_meaning_decorator(False)
    @get_is_something_bigger_decorator(False)
    def __truediv__(self, number):
        new_effects = {}

        for key, effect in self.effects.items():
            if effect.is_depleted:
                continue

            new_effects[key] = effect
            new_effects[key].intensity = Potion.round_half_down(effect.intensity / number)
        
        def create_new_potion():
            new_potion = Potion({}, self.duration)
            copy_new_effects = {}

            for name, effect in new_effects.items():
                copy_new_effects[name] = Effect(name, effect.effect)
                copy_new_effects[name].intensity = effect.intensity
            
            new_potion.effects = copy_new_effects
            return new_potion
        return (create_new_potion() for _ in range(number))
    
    @get_check_for_deep_meaning_decorator(True)
    def __eq__(self, other):
        if(self.effects.keys() != other.effects.keys()):
            return False

        for key, effect in self.effects.items():
            if effect.is_depleted:
                effect.intensity = 0

            if other.effects[key].is_depleted:
                other.effects[key].intensity = 0

            if effect.intensity != other.effects[key].intensity:
                return False
        
        return True
    
    @get_check_for_deep_meaning_decorator(True)
    def __lt__(self, other):
        left_part = sum(effect.intensity if not effect.is_depleted else 0 for effect in self.effects.values())
        right_part = sum(effect.intensity if not effect.is_depleted else 0 for effect in other.effects.values())
        return left_part < right_part
            
    
    @property
    def effects_for_potions(self):
        not_used_effects = filter(lambda effect: not effect.is_depleted, self.effects.values())
        sorted_not_used_effects = sorted(not_used_effects, key=lambda effect: effect.molecule_mass, reverse=True)
        return list(sorted_not_used_effects)
        

    @get_check_for_deep_meaning_decorator(False)
    def apply(self, target):
        self.is_depleted = True
        effects = self.effects_for_potions

        for effect in effects:
            effect(target)

        return effects
    


class EnchantedTarget:
    
    def __init__(self, target):
        self.target = target
        self.target_dict = deepcopy(target.__dict__)
        self.active_potions = []

    def add_potion(self, potion, active_to):
        self.active_potions.append((potion.apply(self.target), active_to))

    def tick(self, time):
        still_active_potions = list(filter(lambda potion: potion[1] > time, self.active_potions))
       
        self.target.__dict__ = deepcopy(self.target_dict)
        for potion in still_active_potions:
            for effect in potion[0]:
                effect.reapply(self.target)
        
        self.active_potions = still_active_potions
    


class ГоспожатаПоХимия:

    def __init__(self):
        self.timer = 0
        self.narcos = {}

    def apply(self, target, potion):
        if potion.duration <= 0:
            return
        
        target_id = id(target)
        if target_id not in self.narcos:
            self.narcos[target_id] = EnchantedTarget(target)

        self.narcos[target_id].add_potion(potion, self.timer + potion.duration)

    def tick(self):
        self.timer += 1

        for enchanted_target in self.narcos.values():
            enchanted_target.tick(self.timer)
