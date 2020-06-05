import random
from math import exp, ceil
class Character():
    def __init__(self, name):
        self.name = name
        self.intelligence = 0
        self.strength = 0
        self.agility = 0
        self.lvl = 0
        self.damage = 5
        self.armor = 0
        self.health = 40 + self.strength*self.lvl
        self.evasion_modify = 0.05
        self.exp = 0
        self.exp_next_lvl = exp(self.lvl)
        self.inventory = []

    def attack(self):
        return [f"*Вы нанесли {self.damage + self.strength} урона*", self.damage + self.str]

    def defend(self):
        d = random.randint(1, 6)
        if d == 5 or d == 6:
            return [f"*Вы полностью заблокировали урон*", True]
        else:
            return [f"*Вы поставили блок, но монстр все равно вас задел*", False]

    def evasion(self):
        chance = (100 + self.agility)*self.evasion_modify
        d = random.randint(1, 100)
        if d < chance:
            return [f"*Вы уклонились от удара*", True]
        else:
            return [f"*Вы не смогли уклониться*", False]


class Warrior(Character):
    def __init__(self, name, strength, agility, intelligence):
        super().__init__(name)
        self.strength = 5 + strength
        self.agility = 3 + agility
        self.intelligence = 2 + intelligence
        self.armor = 5
    def strong_attack(self):
        return [f"*Вы проводите сильный удар, нанося {(self.damage+self.strength)*2}", (self.damage+self.str)*2]

class Mage(Character):
    def __init__(self, name, strength, agility, intelligence):
        super().__init__(name)
        self.strength = 1 + strength
        self.agility = 3 + agility
        self.intelligence = 6 + intelligence
        self.armor = 1

    def fireball(self):
        return [f"*Вы запускаете огненный шар в сушество нанося {10 + self.intelligence} урона*",
                10 + self.intelligence]

class Rogue(Character):
    def __init__(self, name, strength, agility, intelligence):
        super().__init__(name)
        self.strength = 2 + strength
        self.agility = 6 + agility
        self.intelligence = 2 + intelligence
        self.armor = 2
        self.evasion_modify = 0.14

    def backstab(self):
        return [f"*Вы телепортируетесь существу за спину и наносите {10 + self.agility} урона*",
                10 + self.intelligence]


