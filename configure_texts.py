
import configparser

path = "settings.ini"
config = configparser.ConfigParser()
config.read(path)

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()

    config.add_section("Settings")

    config.set("Settings", "terrain", "Вы пришли в {}")

    config.set("Settings", "monster_attack", "Вас атаковал {} на {}")

    config.set("Settings", "hero_attack", "Вы атаковали {} на {}")

    config.set("Settings", "attack", "На вас напал {}")

    config.set("Settings", "hp", "Здоровье: {}/{} ")

    config.set("Settings","create_hero",
"""     
&#128312; Создание персонажа.
&#128312; Вам нужно ввести следующие данные:

&#128313; Ник
&#128313; Класс
&#128313; Характеристики, Вам доступно 7

Например:
Divinity воин 4 2 1
""")

    config.set("Settings","characteristics",
"""
&#128312; Ваш персонаж:

&#128313; Имя: {}
&#128313; Опыт: {}
&#128313; Опыт для лвл апа: {}
&#128313; Уровень: {}

&#128308; Сила: {}
&#10035; Ловкость: {}
&#128160; Интелект: {}

&#128188; Инвентарь:
&#9876; Оружие: {} урон
&#9937; Голова: {} броня
&#128085; Тело: {} броня
&#129508; Руки: {} броня
&#128094; Ноги: {} броня
""")
    #config.set("Config","")
    with open(path, "w") as config_file:
        config.write(config_file)


def Terrain(terr):
    return (config.get("Settings",'Terrain')).format(terr)

def monster_attack(monster,damage):

    return (config.get("Settings",'monster_attack')).format(monster,damage)

def hero_attack(monster,damage):

    return (config.get("Settings",'hero_attack')).format(monster,damage)

def attack(monster):
    return (config.get("Settings", 'attack')).format(monster)


def hp(now,max):
    return (config.get("Settings",'hp')).format(now,max)


def create_hero():
    return config.get("Settings",'create_hero')


def characteristics(nick, exp, exp_next_lvl, lvl, strength, intelligence, agility, weapon, head, body, hands, legs):
    return (config.get("Settings", 'characteristics')).format(nick, exp, exp_next_lvl, lvl, strength,intelligence, agility,
                                                            weapon, head, body, hands, legs)



createConfig(path)
