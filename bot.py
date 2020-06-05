from characters import Warrior, Mage
import random
import sqlite3
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


vkToken = "a244f42cfaacef0f2fc24a253e56023acb0b7ab2f4eb92a3d3678774762aa88114969172edf49b9fa00c9"
admin = 243578504
club = 194548161
conf = 2000000001
conf2 = 2000000003


#Персонажи
characters={

}
# Registration phrases

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




# Create character
def create_character(character, id):
    try:
        conn = sqlite3.connect("characters.db")
        cursor = conn.cursor()
        cursor.execute("insert into characters values(?,?,?,?,?,?,?,?,?)",
                       (id, character.name, character.exp, character.exp_next_lvl, character.lvl, character.str,
                        character.agil, character.int, str(character.inventory)))
        conn.commit()
        conn.close()
        message = f"Ваш персонаж:\n" \
                  f"Имя: {character.name}\n" \
                  f"Опыт: {character.exp}\n" \
                  f"Опыт для лвл апа: {character.exp_next_lvl}\n" \
                  f"Уровень: {character.lvl}\n" \
                  f"Сила: {character.str}\n" \
                  f"Ловкость: {character.agil}\n" \
                  f"Интелект: {character.int}\n" \
                  f"Инвентарь: {str(character.inventory)}\n"
        return message
    except:
        message = "ошибка"
        return message

# Download and Upload
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.message.text.lower() == "!help" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    vk.messages.send(
                        random_id=random.randint(1,10**90),
                        peer_id=peer_id,
                        message=f"Команды:\n"
                                f"🔹 !погода\n"
                                f"🔹 !Шанс (можно писать в любом месте предложения)\n"
                                f"🔹 Ставь лайк\n"
                                f"🔹 !Новости\n"
                                f"🔹 !Кто\n"
                                f"🔹 !Регистрация\n"
                                f"🔹 !Моя анкета\n"
                                f"🔹 !Удалить анкету\n"
                                f"🔹 !Фото\n"
                                f"🔹 !Пик\n"
                                f"🔹 !Поиск\n"
                                f"🔹 !Добавить сервер\n"
                                f"🔹 !График\n"
                                f"🔹 !Созвать\n"
                                f"🔹 !Название\n",
                    )
                elif event.message.text.lower() == "!создать персонажа" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    vk.messages.send(
                        peer_id = peer_id,
                        random_id = random.randint(1,10**90),
                        message = "Сейчас начнется создание персонажа, введите <ник класс сила(число) ловкость(число) интелект(число)> своего персонажа. Точно "
                                  "так же как в примере, только без треугольных скобок. "
                                  "У вас 7 очков чтобы распределить их на силу ловкость и интелект"
                    )
                    condition[event.message.from_id] = "создание персонажа"
                # проверка состояний
                elif event.message.from_id in condition and condition[event.message.from_id] == "создание персонажа":
                    if event.message.text.lower() == "!выход":
                        vk.messages.send(
                            random_id=random.randint(1,10**90),
                            peer_id=event.object.message['peer_id'],
                            message=f"Жаль что мы не поиграем",
                        )
                        condition.pop(event.message.from_id)
                        continue
                    char = event.message.text.split(" ")
                    if char[1].lower() == 'воин':
                        characters[event.message.from_id] = Warrior(char[0],int(char[2]), int(char[3]), int(char[4]))
                    elif char[1].lower() == 'маг':
                        characters[event.message.from_id] = Mage(char[0], int(char[2]), int(char[3]), int(char[4]))
                    mes = create_character(characters[event.message.from_id], event.message.from_id)
                    vk.messages.send(
                        random_id = random.randint(1,10**90),
                        peer_id=event.object.message['peer_id'],
                        message=mes,
                    )
                    condition.pop(event.message.from_id)
    except Exception as err:
        with open("err_log.txt", "a") as log:
            log.write(f"{traceback.format_exc()} {str(datetime.datetime.now())}\n\n")
        vk.messages.send(
            random_id=rand(),
            peer_id=admin,
            message=f"Вылет",
        )
        condition = {}




