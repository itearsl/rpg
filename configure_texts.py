
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

    config.set("Settings", "monster_defeat", "{} повержен")

    config.set("Settings", "hero_defeat", "Вы погибли")  # смерть героя

    config.set("Settings", "hero_attack", "Вы атаковали {} на {}")

    config.set("Settings", "attack", "На вас напал {}")

    config.set("Settings", "hp", "У {} здоровье: {}/{} ")   # Изменил запись

    config.set("Settings", "drop", "Вам выпал предмет {}")

    config.set("Settings", "delete_character", "Ваш персонаж успешно удален")

    config.set("Settings", "error", "Ошибка")

    config.set("Settings", "kd", "Эта способность еще в кулдауне. Осталось {} ходов")

    config.set("Settings", "lvl_up",
'''
&#128313; Уровень повышен!
&#128313; Вы получили 7 очков для повышения характеристик
&#128313; Введите как бы вы хотели их распределить
&#128313; Например: 4 2 1 
&#128313; 4 - в силу, 2 - в ловкость, 1 - в интелект
''')

    config.set("Settings", "help",
'''
Команды:
&#128313; Создать персонажа
&#128313; Мой персонаж
&#128313; Удалить персонажа
&#128313; Охота
&#128313; Путешествие     
''')

    config.set("Settings","create_hero",
"""     
&#128312; Создание персонажа.
&#128312; Вам нужно ввести следующие данные:

&#128313; Ник
&#128313; Класс: Всего 3 - Warrior, Mage, Rogue 
&#128313; Характеристики, доступно 7 - сила, ловкость, интелект.

&#128313; Пример: itearsl Warrior 4 2 1
""")

    config.set("Settings","characteristics",
"""
&#128312; Ваш персонаж:

&#128313; Класс персонажа: {}
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
""") # добавил класс персонажа
    #config.set("Config","")
    with open(path, "w") as config_file:
        config.write(config_file)


def Terrain(terr):
    return (config.get("Settings", 'Terrain')).format(terr)

def monster_attack(monster,damage):
    return (config.get("Settings", 'monster_attack')).format(monster,damage)

def monster_defeat(monster):
    return (config.get("Settings", "monster_defeat")).format(monster)


def hero_defeat():
    return config.get("Settings", "hero_defeat")


def hero_attack(monster,damage):

    return (config.get("Settings", 'hero_attack')).format(monster,damage)


def attack(monster):
    return (config.get("Settings", 'attack')).format(monster)


def hp(character, now, max):    # теперь вывод как для моба, так и для персонажа
    return (config.get("Settings", 'hp')).format(character, now, max)


def create_hero():
    return config.get("Settings", 'create_hero')

def delete_character():
    return config.get("Settings", "delete_character")

def characteristics(person_class, nick, exp, exp_next_lvl, lvl, strength, intelligence, agility, weapon, head, body, hands, legs):
    return (config.get("Settings", 'characteristics')).format(person_class, nick, exp, exp_next_lvl, lvl, strength,intelligence, agility,
                                                            weapon, head, body, hands, legs) # добавил person_class

def drop(item_name):
    return (config.get("Settings", "drop")).format(item_name)

def lvl_up():
    return config.get("Settings", "lvl_up")

def help():
    return config.get("Settings", "help")

def error():
    return config.get("Settings", "error")

def kd(countdown):
    return (config.get("Settings", "kd")).format(countdown)

createConfig(path)
