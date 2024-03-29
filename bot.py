from characters import Warrior, Mage, Rogue
from configure_texts import hero_attack, monster_attack, attack, hero_defeat # импортировал monster_hp, hero_hp, hero_defeat
import configure_texts
import keyboards
from monsters import *
import random
import time
import functools
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import configparser
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import data_base
import asyncio
import logging
from math import exp
import threading

path = "config.ini"
config = configparser.ConfigParser()
config.read(path) # Path

vkToken = config.get("Config",'vkToken')
admin = config.get("Config",'admin')
club = config.get("Config",'club')
#кулдауны
countdowns = {
}
db_len = 15
#Персонажи

#  Init logging config
logging.basicConfig(level=logging.DEBUG, filename='logfile.log', format='%(asctime)s in function: %(funcName)s %(levelname)s:%(message)s ')

characters={
}

#Тут храняться монстры для каждого игрока
mobs = {
}

# Состояния
state = {
}

global condition
condition = {}


# Init vk_api
vk_session = VkApi(token=vkToken)
longpoll = VkBotLongPoll(vk_session, club)
vk = vk_session.get_api()
upload = VkUpload(vk_session)

#init DB
try:
    db = data_base.DB()
except:
    print("Error with connect to database")
    logging.error("Critical error with connect to database")
    exit(1)

#init keyboads class
kb = keyboards.KB()
async def load_characters_f():

    chars = await db.load_characters()
    for character in chars:
        id_user = character[0]
        if len(character) != db_len:
            logging.error("Error, we have {} elements at database, but normal result {}".format(len(character), db_len))
            print("Error, we have {} elements at database, but normal result {}".format(len(character), db_len))
            continue
        characters[id_user] = globals()[character[8]](character[1], int(character[5]), int(character[6]), int(character[7]))
        characters[id_user].strength = int(character[5])
        characters[id_user].agility = int(character[6])
        characters[id_user].intelligence = int(character[7])
        characters[id_user].exp = int(character[2])
        characters[id_user].exp_next_lvl = int(character[3])
        characters[id_user].lvl = int(character[4])
        characters[id_user].money = int(character[14])

        list_armor = []

        for i in range(9, 14):
            list_armor.append(int(character[i].split("-")[1]))
        armor = sum(list_armor)
        damage = int(character[9].split("-")[1])

        characters[id_user].damage += damage
        characters[id_user].armor += armor

async def equipment_comparison(id, equip):
    equiped_item = await db.get_equip(equip[1], id)#получаем надетый сейчас предмет
    value = int(equiped_item[0].split("-")[1])
    if equip[2] > value: #сравниваем показатель
        await db.change_equip(id, equip)
        if equip[0].lower() != "weapon":
            characters[id].armor += equip[2] - value
        else:
            characters[id].damage += equip[2] - value
    else:
        characters[id].money += 10*equip[3]

async def lvl_up(character, characteristics, peer_id):
    if check_lvl_up(characteristics)[-1]:
        character.lvl += 1
        character.exp = 0
        character.exp_next_lvl = round(exp(character.lvl))
        character.strength += int(characteristics[0])
        character.agility += int(characteristics[1])
        character.intelligence += int(characteristics[2])
        character.health = 40 + character.strength*character.lvl
        character.max_health = character.health
        vk_message("Уровень успешно увеличен!", peer_id)
    else:
        vk_message(check_lvl_up(characteristics)[0], peer_id)

async def fight_checks(from_id, peer_id, hero_damage, monster_damage, fight_keyboard):
    vk_message(hero_attack(mobs[from_id].name, hero_damage),
               peer_id)  # Отправляет сколько и кому нанес урон герой
    if mobs[from_id].health <= 0:
        vk_message(configure_texts.monster_defeat(mobs[from_id].name),
                   peer_id) # Извещение о смерти моба
        condition.pop(from_id)
        item = await db.get_item(characters[from_id].lvl)
        vk_message(configure_texts.drop(item[0]), peer_id, kb.choice_keyboard)
        await equipment_comparison(from_id, item)
        characters[from_id].exp += mobs[from_id].exp
        if characters[from_id].exp >= characters[from_id].exp_next_lvl:
            condition[from_id] = "lvl_up"
            vk_message(configure_texts.lvl_up(), peer_id)
        mobs.pop(from_id)
    else:
        vk_message(
            configure_texts.hp(mobs[from_id].name, mobs[from_id].health,
                               mobs[from_id].max_health),
            peer_id)  # Отправляет сколько хп осталось у моба
        vk_message(monster_attack(mobs[from_id].name, monster_damage),
                   peer_id)  # Отправляет какой моб и сколько урона нанёс урона герою
        if characters[from_id].health <= 0:
            vk_message(configure_texts.hero_defeat(), peer_id)
            condition.pop(from_id)  # Извещение о смерти героя
        else:
            vk_message(configure_texts.hp(characters[from_id].name,
                                          characters[from_id].health,
                                          characters[from_id].max_health),
                       peer_id,
                       fight_keyboard)  # Отправляет сколько хп осталось у персонажа

def save_characters():
    threading.Timer(30.0, save_characters).start()
    for character in characters:
        db.save_characters(characters[character], character)

def vk_message(*args):

    if len(args) == 2:
        vk.messages.send(
            random_id=get_random_id(),
            peer_id=args[1],
            message=args[0]
        )
    elif len(args) == 3:
        vk.messages.send(
            peer_id=args[1],
            random_id=get_random_id(),
            keyboard=args[2].get_keyboard(),
            message=args[0]
        )
async def attack_with_armor(monster_damage, from_id):
    if monster_damage > characters[from_id].armor:
        characters[from_id].health += characters[from_id].armor - monster_damage
    else:
        characters[from_id].health -= 0
async def countdown_reduction(countdowns):
    for kd in countdowns:
        kd -= 1
def check_lvl_up(message):
    if len(message) != 3:
        return "Пожалуйста, введите данные по примеру, например 4 2 1", False
    strength = message[0]
    agility = message[1]
    intelligence = message[2]
    if strength.isdigit() and agility.isdigit() and intelligence.isdigit():
        if int(strength) + int(agility) + int(intelligence) != 7:
            return "Сумма характеристик должна быть равна 7, пожалуйста введите характеристики через пробел, например 4 2 1", False
        return "Отлично, вы правильно ввели характеристики!", True
    return "Пожалуйста, введите числами характеристики, например 4 2 1", False
def check_characters(message):
    """Check  characters validate"""
    if len(message) != 5:
        return "Пожалуйста, введите данные по примеру, например bot воин 4 2 1", False
    strength = message[2]
    agility = message[3]
    intelligence = message[4]
    if strength.isdigit() and agility.isdigit() and intelligence.isdigit():
        if int(strength) + int(agility) + int(intelligence) != 7:
            return "Сумма характеристик должна быть равна 7, пожалуйста введите характеристики через пробел, например 4 2 1", False
        return "Отлично, вы правильно ввели характеристики!", True
    return "Пожалуйста, введите числами характеристики, например bot воин 4 2 1", False


async def bot_cycle():
    global condition
    load_characters = True
    while True:
        # try:
            if load_characters:
                load_characters = False
                await load_characters_f()
                save_characters()
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    logging.debug("We got new message from: {}. Text message: {}".format(event.message.from_id, event.message.text))
                    if event.message.text.lower() == "help" and event.message.from_id not in condition:
                        peer_id = event.object.message['peer_id']
                        vk_message(configure_texts.help(), peer_id)
                    elif event.message.text.lower() == "создать персонажа" and event.message.from_id not in condition:
                        peer_id = event.object.message['peer_id']
                        vk_message(configure_texts.create_hero(), peer_id)
                        condition[event.message.from_id] = "создание персонажа"
                    elif event.message.text.lower() == "мой персонаж" and event.message.from_id not in condition:
                        mes_char = await db.show_character(event.message.from_id)
                        vk_message(mes_char, event.object.message['peer_id'])
                    elif event.message.text.lower() == "охота" and event.message.from_id not in condition:
                        condition[event.message.from_id] = "охота"
                        countdowns[event.message.from_id] = [0, 0, 0, 0]
                        mob = await db.get_monster(characters[event.message.from_id].current_location) #Получаем моба из текущей локации
                        mobs[event.message.from_id] = globals()[mob[0]](random.randint(characters[event.message.from_id].lvl-2,
                                                                                       characters[event.message.from_id].lvl+3)) #Создаем моба
                        fight_keyboard = await kb.fight_keyboard(characters[event.message.from_id])
                        vk_message(attack(mobs[event.message.from_id].name), event.object.message["peer_id"], fight_keyboard)
                    elif event.message.text.lower() == "удалить персонажа" and event.message.from_id not in condition:
                        del_message = await db.delete_character(event.message.from_id)
                        vk_message(del_message, event.object.message["peer_id"])
                    elif event.message.text.lower() == "путешествие" and event.message.from_id not in condition:
                        condition[event.message.from_id] = "путешествие"
                        locations = await db.get_locations()
                        tr_keyboard = await kb.travel_keyboard(locations)
                        vk_message("Куда вы хотите отправиться?", event.object.message["peer_id"], tr_keyboard)
                    elif event.message.text.lower() == "вернуться в дрифтвуд" and event.message.from_id not in condition:
                        characters[event.message.from_id].current_location = "Дрифтвуд" #Меняем текущую локацию персонажа
                        vk_message(configure_texts.Terrain("Дрифтвуд"), event.object.message["peer_id"], kb.town_keyboard) #Сообщение о прибытии в город и вывод городской клавы
                    # проверка состояний
                    elif event.message.from_id in condition and condition[event.message.from_id] == "создание персонажа":
                        if event.message.text.lower() == "выход":
                            vk_message("Жаль что мы не поиграем", event.object.message["peer_id"])
                            condition.pop(event.message.from_id, event.object.message["peer_id"])
                            continue

                        char = event.message.text.split(" ")
                        """В отдельной функции надо сделать"""
                        if check_characters(char)[-1]:
                            characters[event.message.from_id] = globals()[char[1]](char[0], int(char[2]), int(char[3]), int(char[4]))
                        else:
                            vk_message(check_characters(char)[0], event.object.message["peer_id"])
                            continue

                            # ВОЗМОЖНО ОШИБКА БУДЕТ, НАДО ПРОВЕРИТЬ. НЕ УДАЛЯТЬ ПОКА НЕ ПРОВЕРЕННО


                        mes = await db.create_character(characters[event.message.from_id], event.message.from_id)
                        vk_message(mes, event.object.message["peer_id"])
                        condition.pop(event.message.from_id)
                    elif event.message.from_id in condition and condition[event.message.from_id] == "охота":
                        fight_keyboard = await kb.fight_keyboard(characters[event.message.from_id])
                        monster_damage = mobs[event.message.from_id].attack()
                        await attack_with_armor(monster_damage, event.message.from_id)
                        if event.message.text.lower() == "удар":
                            hero_damage = characters[event.message.from_id].attack()    # Урон героя
                        elif event.message.text.lower() == "огненный шар":
                            if countdowns[event.message.from_id][0] == 0:
                                hero_damage = characters[event.message.from_id].fireball()    # Урон героя
                                countdowns[event.message.from_id][0] = 2
                            else:
                                hero_damage = 0
                                vk_message(configure_texts.kd(countdowns[event.message.from_id][0]), event.message.from_id, fight_keyboard)
                                continue
                        elif event.message.text.lower() == "сильный удар":
                            if countdowns[event.message.from_id][0] == 0:
                                hero_damage = characters[event.message.from_id].strong_attack()    # Урон героя
                                countdowns[event.message.from_id][0] = 2
                            else:
                                hero_damage = 0
                                vk_message(configure_texts.kd(countdowns[event.message.from_id][0]), event.message.from_id, fight_keyboard)
                                continue
                        elif event.message.text.lower() == "удар в спину":
                            if countdowns[event.message.from_id][0] == 0:
                                hero_damage = characters[event.message.from_id].backstab()  # Урон героя
                                countdowns[event.message.from_id][0] = 2
                            else:
                                hero_damage = 0
                                vk_message(configure_texts.kd(countdowns[event.message.from_id][0]), event.message.from_id, fight_keyboard)
                                continue
                        mobs[event.message.from_id].health -= hero_damage  # вычитает из хп моба урона от героя
                        await countdown_reduction(countdowns[event.message.from_id])
                        await fight_checks(event.message.from_id, event.object.message["peer_id"], hero_damage,
                                           monster_damage, fight_keyboard)
                    elif event.message.from_id in condition and condition[event.message.from_id] == "путешествие":
                        desc = await db.get_desc(event.message.text) #Получаем описание локации
                        characters[event.message.from_id].current_location = event.message.text #Меняем текущую локацию перснажа
                        vk_message(configure_texts.Terrain(event.message.text), event.object.message["peer_id"])
                        vk_message(desc, event.object.message["peer_id"], kb.choice_keyboard) #Выводим описание и клавиатуру
                        condition.pop(event.message.from_id)
                    elif event.message.from_id in condition and condition[event.message.from_id] == "lvl_up":
                        characteristics = event.message.text.split(" ")
                        condition.pop(event.message.from_id)
                        await lvl_up(characters[event.message.from_id], characteristics,
                                     event.object.message['peer_id'])


        # except Exception as err:
        #
        #     logging.error("Critical error", exc_info=True)
        #     vk_message("Мы получили критическую ошибку, запись в логе", admin)
        #     condition = {}


async def main():
    bot_cycle_task = asyncio.create_task(bot_cycle())
    await asyncio.gather(bot_cycle_task)

if __name__ == '__main__':
    asyncio.run(main())



