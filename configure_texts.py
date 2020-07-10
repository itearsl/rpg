
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

    config.set("Settings", "attack", "Вас атаковал {} на {}")

    config.set("Settings", "hp", "Здоровье: {}/{} ")

    config.set("Settings","create_hero",
"""     
&#128312; Создание персонажа.
&#128312; Вам нужно ввести следующие данные:

&#128313; Ник
&#128313; Класс
&#128313; Характеристики, доступно 7, вводите через кнопки.
КНОПКИ: СИЛА ЛОВКОСТЬ ИНТЕЛЛЕКТ
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

def Attack(monster,damage):

    return (config.get("Settings",'attack')).format(monster,damage)

def hp(now,max):
    return (config.get("Settings",'hp')).format(now,max)


def create_hero():
    return config.get("Settings",'create_hero')


def characteristics(nick, exp, exp_next_lvl, lvl, strength, intelligence, agility, weapon, head, body, hands, legs):
    return (config.get("Settings", 'characteristics')).format(nick, exp, exp_next_lvl, lvl, strength,intelligence, agility,
                                                            weapon, head, body, hands, legs)



createConfig(path)
