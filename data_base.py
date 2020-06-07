import asyncio
import pymysql
import configure_texts

con = pymysql.connect(host='localhost',
                    user='root',
                    passwd='qwe13245',
                    db='rpg',
                    charset="utf8",
                    port=3528)

# Класс для управления БД
class DB():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                    user='root',
                    passwd='qwe13245',
                    db='rpg',
                    charset="utf8",
                    port=3528)
        self.cur = self.conn.cursor()
    # Записываем персонажа в БД
    async def create_character(self, character, id):
        # try:
            self.cur.execute("insert into characters values(%s,%s,%s,%s,%s,%s,%s,%s)",
                           (
                           id, character.name, character.exp, character.exp_next_lvl, character.lvl, character.strength,
                           character.agility, character.intelligence))
            self.conn.commit()
            message = configure_texts.characteristics(character.name, character.exp, character.exp_next_lvl,
                                                      character.lvl, character.strength,
                                                      character.agility, character.intelligence)
            return message
        # except:
        #     message = "ошибка"
        #     return message
    def close(self):
        self.conn.close()