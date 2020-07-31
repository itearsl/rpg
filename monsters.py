import random

class Monster():
    def __init__(self, lvl):
        self.lvl = lvl or 1
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
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Гоблин"
        self.damage = 1 + self.lvl*2
        self.health = 13 + self.lvl*2
        self.exp = 0.25*self.lvl
        self.max_health = 13 + self.lvl * 2


class Skeleton(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Скелет"
        self.damage = 2 + self.lvl*2
        self.exp = 0.25*self.lvl
        self.health = 15 + self.lvl*2
        self.max_health = 15 + self.lvl * 2

class Grog(Monster):
    def __init__(self, name, lvl):
        super().__init__(lvl)
        self.name = "Грог"
        self.damage = 5 + self.lvl*2
        self.exp = 0.25 + 0.25*self.lvl
        self.health = 23 + self.lvl*2
        self.max_health = 23 + self.lvl * 2

class King_fire_slug(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Огненная королевская слизь"
        self.damage = 8 + self.lvl*2
        self.health = 28 + self.lvl*2
        self.exp = 0.25 + 0.25*self.lvl
        self.max_health = 28 + self.lvl * 2

class Vile_fiend(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Мерзкое исчадие ада"
        self.damage = 6 + self.lvl*2
        self.health = 21 + self.lvl*2
        self.exp = 1 + 0.25*self.lvl
        self.max_health = 21 + self.lvl * 2

class Troll(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Тролль"
        self.damage = 13 + self.lvl*2
        self.health = 13 + self.lvl * 2
        self.exp = 1 + 0.25*self.lvl
        self.max_health = 13 + self.lvl*2

class Bear(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Медведь"
        self.damage = 16 + self.lvl*2
        self.health = 40 + self.lvl*2
        self.exp = 1.25 + 0.25*self.lvl
        self.max_health = 40 + self.lvl*2

class Algul(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Альгуль"
        self.damage = 22 + self.lvl*2
        self.health = 46 + self.lvl * 2
        self.exp = 1.5 + 0.25*self.lvl
        self.max_health = 46 + self.lvl*2

class Demon(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Бес"
        self.damage = 20 + self.lvl*2
        self.health = 42 + self.lvl * 2
        self.exp = 1.5 + 0.25*self.lvl
        self.max_health = 42 + self.lvl*2

class Big_bad_wolf(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Большой злой волк"
        self.damage = 25 + self.lvl*2
        self.health = 48 + self.lvl * 2
        self.exp = 2 + 0.25*self.lvl
        self.max_health = 48 + self.lvl*2

class Scavenger(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Падальщик"
        self.damage = 27 + self.lvl*2
        self.health = 50 + self.lvl * 2
        self.exp = 2.25 + 0.25*self.lvl
        self.max_health = 50 + self.lvl*2

class Devourer(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Пожиратель"
        self.damage = 32 + self.lvl*2
        self.health = 54 + self.lvl * 2
        self.exp = 2.5 + 0.25*self.lvl
        self.max_health = 54 + self.lvl*2

class Vampire(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Вампир"
        self.damage = 34 + self.lvl*2
        self.health = 56 + self.lvl * 2
        self.exp = 3 + 0.25*self.lvl
        self.max_health = 56 + self.lvl*2

class Varg(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Варг"
        self.damage = 36 + self.lvl*2
        self.health = 62 + self.lvl * 2
        self.exp = 3.25 + 0.25*self.lvl
        self.max_health = 62 + self.lvl*2

class Ghost(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Призрак"
        self.damage = 36 + self.lvl*2
        self.health = 60 + self.lvl * 2
        self.exp = 3.5 + 0.25*self.lvl
        self.max_health = 60 + self.lvl*2

class Wyvern(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Виверна"
        self.damage = 40 + self.lvl*2
        self.health = 64 + self.lvl * 2
        self.exp = 3.75 + 0.25*self.lvl
        self.max_health = 64 + self.lvl*2

class Boar(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Вепрь"
        self.damage = 46 + self.lvl*2
        self.health = 68 + self.lvl * 2
        self.exp = 4 + 0.25*self.lvl
        self.max_health = 68 + self.lvl*2

class Golem(Monster):
    def __init__(self, lvl):
        super().__init__(lvl)
        self.name = "Голем"
        self.damage = 50 + self.lvl*2
        self.health = 74 + self.lvl * 2
        self.exp = 4.25 + 0.25*self.lvl
        self.max_health = 74 + self.lvl*2