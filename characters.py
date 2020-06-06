import random
from math import exp, ceil
class Character():
    def __init__(self, name):
        self.name = name
        self.intelligence = 0
        self.strength = 0
        self.agility = 0
        self.lvl = 1  # УРОВЕНЬ НАЧИНАЕТСЯ С 1
        self.damage = 5
        self.armor = 0
        self.health = 40 + self.strength*self.lvl
        self.evasion_modify = 0.05
        self.exp = 0
        self.exp_next_lvl = exp(self.lvl)
        self.inventory = []

    def attack(self):
        return self.damage + self.strength

    def defend(self):
        d = random.randint(1, 6)
        if d > 4:
            return True

        return False

    def evasion(self):
        chance = (100 + self.agility)*self.evasion_modify
        d = random.randint(1, 100)
        if d < chance:
            return True
        else:
            return False


class Warrior(Character):
    def __init__(self, name, strength, agility, intelligence):
        super().__init__(name)
        self.strength = 5 + strength
        self.agility = 3 + agility
        self.intelligence = 2 + intelligence
        self.armor = 5
    def strong_attack(self):
        return (self.damage+self.strength)*2

class Mage(Character):
    def __init__(self, name, strength, agility, intelligence):
        super().__init__(name)
        self.strength = 1 + strength
        self.agility = 3 + agility
        self.intelligence = 6 + intelligence
        self.armor = 1

    def fireball(self):
        return 10 + self.intelligence

class Rogue(Character):
    def __init__(self, name, strength, agility, intelligence):
        super().__init__(name)
        self.strength = 2 + strength
        self.agility = 6 + agility
        self.intelligence = 2 + intelligence
        self.armor = 2
        self.evasion_modify = 0.14

    def backstab(self):
        return 10 + self.intelligence


