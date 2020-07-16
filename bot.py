from characters import Warrior, Mage, Rogue
from configure_texts import hero_attack, monster_attack, attack, monster_hp, hero_hp, hero_defeat # импортировал monster_hp, hero_hp, hero_defeat
import configure_texts
from monsters import Troll, King_fire_slug, Skeleton, Goblin, Vile_fiend, Grog
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import traceback
import datetime
import configparser
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import data_base
import asyncio
import logging

path = "config.ini"
config = configparser.ConfigParser()
config.read(path) # Path

vkToken = config.get("Config",'vkToken')
admin = config.get("Config",'admin')
club = config.get("Config",'club')



db_len = 14
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

condition = {
}


# Init vk_api
vk_session = VkApi(token=vkToken)
longpoll = VkBotLongPoll(vk_session, club)
vk = vk_session.get_api()
upload = VkUpload(vk_session)
fight_keyboard = VkKeyboard(one_time=False, inline=True)

fight_keyboard.add_button('атака', color=VkKeyboardColor.DEFAULT)
#init DB
try:
    db = data_base.DB()
except:
    print("Error with connect to database")
    logging.error("Critical error with connect to database")
    exit(1)
async def load_characters_f():

    """Все равно пока говно, я подумаю как сделать лучше"""

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

        list_armor = []

        for i in range(9, 14):
            list_armor.append(int(character[i].split("-")[1]))
        armor = sum(list_armor)
        damage = int(character[9].split("-")[1])

        characters[id_user].damage += damage
        characters[id_user].armor += armor


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
        try:
            if load_characters:
                load_characters = False
                await load_characters_f()
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    logging.debug("We got new message from: {}. Text message: {}".format(event.message.from_id,event.message.text))
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
                    elif event.message.text.lower() == "бой" and event.message.from_id not in condition:
                        condition[event.message.from_id] = "бой"
                        mob = await db.get_monster()
                        mobs[event.message.from_id] = globals()[mob[0]](characters[event.message.from_id].lvl)
                        vk_message(attack(mobs[event.message.from_id].name), event.object.message["peer_id"], fight_keyboard)
                    elif event.message.text.lower() == "удалить персонажа" and event.message.from_id not in condition:
                        del_message = await db.delete_character(event.message.from_id)
                        vk_message(del_message, event.object.message["peer_id"])
                    elif event.message.text.lower() == "предметы" and event.message.from_id not in condition and (event.message.from_id == 176803261 or event.message.from_id == admin):
                        vk.messages.send(
                            random_id=random.randint(1, get_random_id()),
                            peer_id=event.object.message['peer_id'],
                            message="можешь начинать(!выход для остановки). Вводи в таком вормате:"
                                    "<название lvl тип(оружие/броня) значение(урон/защита)>\n"
                                    "Пример: меч 2 оружие 3\n"
                                    "надеюсь ты понял",
                        )
                        condition[event.message.from_id] = "предметы"
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
                    elif event.message.from_id in condition and condition[event.message.from_id] == "предметы":
                        if event.message.text.lower() == "выход":
                            vk.messages.send(
                                random_id=get_random_id(),
                                peer_id=event.object.message['peer_id'],
                                message="Жаль что мы не поиграем",
                            )
                            condition.pop(event.message.from_id)
                            continue
                        item = event.message.text.split(" ")
                        await db.add_item(item)
                        vk.messages.send(
                            random_id=get_random_id(),
                            peer_id=event.object.message['peer_id'],
                            message="Предмет добавлен",
                        )
                    elif event.message.from_id in condition and condition[event.message.from_id] == "бой":
                        if event.message.text.lower() == "атака":
                            hero_damage = characters[event.message.from_id].attack()    # Урон героя
                            monster_damage = mobs[event.message.from_id].attack()   # Урон монстра
                            mobs[event.message.from_id].health -= hero_damage  # вычитает из хп моба урона от героя
                            characters[
                                event.message.from_id].health -= monster_damage  # Вычитает из хп героя урон от моба
                            vk_message(hero_attack(mobs[event.message.from_id].name, hero_damage),
                                       event.object.message['peer_id'])  # Отправляет сколько и кому нанес урон герой
                            if mobs[event.message.from_id].health <= 0:
                                vk_message(configure_texts.monster_defeat(mobs[event.message.from_id].name),
                                           event.object.message["peer_id"])
                                condition.pop(event.message.from_id)    # Извещение о смерти моба
                                continue
                            else:
                                vk_message(
                                    configure_texts.hp(mobs[event.message.from_id].name, mobs[event.message.from_id].health,
                                                       mobs[event.message.from_id].max_health),
                                    event.object.message['peer_id']) # Отправляет сколько хп осталось у моба
                                vk_message(monster_attack(mobs[event.message.from_id].name, monster_damage),
                                           event.object.message[
                                               'peer_id'])  # Отправляет какой моб и сколько урона нанёс урона герою
                                if characters[event.message.from_id].health <= 0:
                                    vk_message(configure_texts.hero_defeat(), event.object.message["peer_id"])
                                    condition.pop(event.message.from_id)    # Извещение о смерти героя
                                    continue
                                else:
                                    vk_message(configure_texts.hp(characters[event.message.from_id].name,
                                                                  characters[event.message.from_id].health,
                                                                  characters[event.message.from_id].max_health),
                                               event.object.message['peer_id'],
                                               fight_keyboard)  # Отправляет сколько хп осталось у персонажа
                                    continue

        except Exception as err:

            logging.error("Critical error", exc_info=True)
            vk_message("Мы получили критическую ошибку, запись в логе", admin)
            condition = {}


async def main():
    bot_cycle_task = asyncio.create_task(bot_cycle())
    await asyncio.gather(bot_cycle_task)

if __name__ == '__main__':
    asyncio.run(main())



