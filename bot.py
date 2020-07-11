from characters import Warrior, Mage, Rogue
from configure_texts import hero_attack, monster_attack
import monsters
import random
import traceback
import datetime
import configparser
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import data_base
import asyncio

path = "config.ini"
config = configparser.ConfigParser()
config.read(path)

vkToken = config.get("Config",'vkToken')
admin = config.get("Config",'admin')
club = config.get("Config",'club')

random_number_message = 10 ** 100


db_len = 14
#Персонажи
characters={

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

#init DB
db = data_base.DB()



async def load_characters_f():

    """Все равно пока говно, я подумаю как сделать лучше"""

    chars = await db.load_characters()
    for character in chars:
        id_user = character[0]
        if len(character) != db_len:
            print("Error, we have {} elements at database, but normal result {}".format(len(character), db_len))  #WRITE TO LOG TOO!!!!
            continue
        if character[8] == 'Warrior':
            characters[id_user] = Warrior(character[1], int(character[5]), int(character[6]), int(character[7]))
        elif character[8] == 'Mage':
            characters[id_user] = Mage(character[1], int(character[5]), int(character[6]), int(character[7]))
        elif character[8] == 'Rogue':
            characters[id_user] = Rogue(character[1], int(character[5]), int(character[6]), int(character[7]))
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

def vk_mssage(mes, peer_id):
    vk.messages.send(
        random_id = random.randint(1, random_number_message),
        peer_id = peer_id,
        message = mes
    )

gob = monsters.Goblin("гоблин", 1)
async def bot_cycle():
    load_characters = True
    while True:
        # try:
            if load_characters == True:
                load_characters = False
                await load_characters_f()
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.message.text.lower() == "!help" and event.message.from_id not in condition:
                        condition[event.message.from_id] = "бой"
                        peer_id = event.object.message['peer_id']
                        vk.messages.send(
                            random_id=random.randint(1, random_number_message),
                            peer_id=peer_id,
                            message="Команды:\n"
                                    "🔹 !Создать персонажа"
                        )
                    elif event.message.text.lower() == "!создать персонажа" and event.message.from_id not in condition:
                        peer_id = event.object.message['peer_id']
                        vk.messages.send(
                            peer_id=peer_id,
                            random_id=random.randint(1, random_number_message),
                            message="Сейчас начнется создание персонажа, введите <ник класс сила(число) ловкость(число) интелект(число)> своего персонажа. Точно "
                                    "так же как в примере, только без треугольных скобок. "
                                    "У вас 7 очков чтобы распределить их на силу ловкость и интелект"
                        )
                        condition[event.message.from_id] = "создание персонажа"
                    elif event.message.text.lower() == "!мой персонаж" and event.message.from_id not in condition:
                        mes_char = await db.show_character(event.message.from_id)
                        vk.messages.send(
                            random_id=random.randint(1, random_number_message),
                            peer_id=event.object.message['peer_id'],
                            message=mes_char,
                        )
                    elif event.message.text.lower() == "!удалить персонажа" and event.message.from_id not in condition:
                        del_message = await db.delete_character(event.message.from_id)
                        vk.messages.send(
                            random_id = random.randint(1, random_number_message),
                            peer_id = event.object.message["peer_id"],
                            message = del_message,
                        )
                    elif event.message.text.lower() == "!предметы" and event.message.from_id not in condition and (event.message.from_id == 176803261 or event.message.from_id == admin):
                        vk.messages.send(
                            random_id=random.randint(1, random_number_message),
                            peer_id=event.object.message['peer_id'],
                            message="можешь начинать(!выход для остановки). Вводи в таком вормате:"
                                    "<название lvl тип(оружие/броня) значение(урон/защита)>\n"
                                    "Пример: меч 2 оружие 3\n"
                                    "надеюсь ты понял",
                        )
                        condition[event.message.from_id] = "предметы"
                    # проверка состояний
                    elif event.message.from_id in condition and condition[event.message.from_id] == "создание персонажа":
                        if event.message.text.lower() == "!выход":
                            vk.messages.send(
                                random_id=random.randint(1, random_number_message),
                                peer_id=event.object.message['peer_id'],
                                message="Жаль что мы не поиграем",
                            )
                            condition.pop(event.message.from_id)
                            continue
                        char = event.message.text.split(" ")
                        if char[1].lower() == 'воин':
                            characters[event.message.from_id] = Warrior(char[0], int(char[2]), int(char[3]), int(char[4]))
                        elif char[1].lower() == 'маг':
                            characters[event.message.from_id] = Mage(char[0], int(char[2]), int(char[3]), int(char[4]))
                        elif char[1].lower() == 'разбойник':
                            characters[event.message.from_id] = Rogue(char[0], int(char[2]), int(char[3]), int(char[4]))
                        else:
                            vk.messages.send(
                                random_id=random.randint(1, random_number_message),
                                peer_id=event.object.message['peer_id'],
                                message="такого класса нет в игре",
                            )
                            condition.pop(event.message.from_id)
                            continue
                        mes = await db.create_character(characters[event.message.from_id], event.message.from_id)
                        vk.messages.send(
                            random_id=random.randint(1, random_number_message),
                            peer_id=event.object.message['peer_id'],
                            message=mes,
                        )
                        condition.pop(event.message.from_id)
                    elif event.message.from_id in condition and condition[event.message.from_id] == "предметы":
                        if event.message.text.lower() == "!выход":
                            vk.messages.send(
                                random_id=random.randint(1, random_number_message),
                                peer_id=event.object.message['peer_id'],
                                message="Жаль что мы не поиграем",
                            )
                            condition.pop(event.message.from_id)
                            continue
                        item = event.message.text.split(" ")
                        await db.add_item(item)
                        vk.messages.send(
                            random_id=random.randint(1, random_number_message),
                            peer_id=event.object.message['peer_id'],
                            message="Предмет добавлен",
                        )
                    elif event.message.from_id in condition and condition[event.message.from_id] == "бой":
                        if gob.health <= 0:
                            vk.messages.send(
                                random_id=random.randint(1, random_number_message),
                                peer_id=event.object.message['peer_id'],
                                message="Монстр был повержен"
                            )
                            condition.pop(event.message.from_id)
                            continue
                        else:
                            if event.message.text.lower() == "атака":
                                hero_damage = characters[event.message.from_id].attack()
                                monster_damage = gob.attack()
                                vk_mssage(hero_attack(gob.name, hero_damage), event.object.message['peer_id'])
                                vk_mssage(monster_attack(gob.name, monster_damage), event.object.message['peer_id'])
                                gob.health -= hero_damage
                                continue



        # except Exception as err:
        #     with open("err_log.txt", "a") as log:
        #         log.write("{} {}\n\n".format(traceback.format_exc(), str(datetime.datetime.now())))
        #     vk.messages.send(
        #         random_id=random.randint(1,10**90),
        #         peer_id=admin,
        #         message="Вылет",
        #     )
        #     condition = {}


async def main():
    bot_cycle_task = asyncio.create_task(bot_cycle())
    await asyncio.gather(bot_cycle_task)

if __name__ == '__main__':
    asyncio.run(main())



