import random

class Monster():
    def __init__(self, name):
        self.name = name
        self.lvl = 1
        self.health = 15 + 2*self.lvl
        self.damage = 5
        self.armor = 0
        self.evasion_modify = 0.03
    def attack(self):
        return (self.damage)
    def evasion(self):
        chance = 100 * self.evasion_modify
        d = random.randint(1, 100)
        if d < chance:
            return True
        else:
            return False


class Goblin(Monster):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 1 + self.lvl*2
        self.health = 13 + self.lvl*2


class Skeleton(Monster):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 2 + self.lvl*2
        self.health = 15 + self.lvl*2

class Grog(Monster):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 5 + self.lvl*2
        self.health = 23 + self.lvl*2

class King_fire_slug(Monster):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 8 + self.lvl*2
        self.health = 28 + self.lvl*2

class Vile_fiend(Monster):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 6 + self.lvl*2
        self.health = 21 + self.lvl*2

class Troll(Monster):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 13 + self.lvl*2
        self.health = 38 + self.lvl*2
