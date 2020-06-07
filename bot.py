from characters import Warrior, Mage
import random
import traceback
import datetime
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import data_base
import asyncio

vkToken = "a244f42cfaacef0f2fc24a253e56023acb0b7ab2f4eb92a3d3678774762aa88114969172edf49b9fa00c9"
admin = 243578504
club = 194548161

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

#init DB
db = data_base.DB()

async def bot_sycle():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.message.text.lower() == "!help" and event.message.from_id not in condition:
                        peer_id = event.object.message['peer_id']
                        vk.messages.send(
                            random_id=random.randint(1, 10 ** 90),
                            peer_id=peer_id,
                            message="Команды:\n"
                                    "🔹 !Создать персонажа"
                        )
                    elif event.message.text.lower() == "!создать персонажа" and event.message.from_id not in condition:
                        peer_id = event.object.message['peer_id']
                        vk.messages.send(
                            peer_id=peer_id,
                            random_id=random.randint(1, 10 ** 90),
                            message="Сейчас начнется создание персонажа, введите <ник класс сила(число) ловкость(число) интелект(число)> своего персонажа. Точно "
                                    "так же как в примере, только без треугольных скобок. "
                                    "У вас 7 очков чтобы распределить их на силу ловкость и интелект"
                        )
                        condition[event.message.from_id] = "создание персонажа"
                    # проверка состояний
                    elif event.message.from_id in condition and condition[event.message.from_id] == "создание персонажа":
                        if event.message.text.lower() == "!выход":
                            vk.messages.send(
                                random_id=random.randint(1, 10 ** 90),
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
                        mes = await db.create_character(characters[event.message.from_id], event.message.from_id)
                        vk.messages.send(
                            random_id=random.randint(1, 10 ** 90),
                            peer_id=event.object.message['peer_id'],
                            message=mes,
                        )
                        condition.pop(event.message.from_id)
        except Exception as err:
            with open("err_log.txt", "a") as log:
                log.write("{} {}\n\n".format(traceback.format_exc(), str(datetime.datetime.now())))
            vk.messages.send(
                random_id=random.randint(1,10**90),
                peer_id=admin,
                message=f"Вылет",
            )
            condition = {}


async def main():
    bot_cycle_task = asyncio.create_task(bot_sycle())
    await asyncio.gather(bot_cycle_task)

# Download and Upload

if __name__ == '__main__':
    asyncio.run(main())



