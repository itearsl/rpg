import asyncio
import random
import pymysql
import configure_texts

# Класс для управления БД
class DB():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                    user='root',
                    passwd='password',
                    db='rpg',
                    charset="utf8")
        self.cur = self.conn.cursor()
    # Записываем персонажа в БД
    async def create_character(self, character, id):
        # try:
            self.cur.execute("insert into characters values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (
                           id, character.name, character.exp, character.exp_next_lvl, character.lvl, character.strength,
                           character.agility, character.intelligence, id, character.specialist))
            self.cur.execute('insert into inventory values(%s,"кинжал-2","пусто-0","порваная накидка-2","пусто-0","лапти-1")',
                             (id))
            self.conn.commit()
            message = configure_texts.characteristics(character.name, character.exp, character.exp_next_lvl,
                                                      character.lvl, character.strength,
                                                      character.agility, character.intelligence,
                                                      "кинжал-2","пусто-0","порваная накидка-2","пусто-0","лапти-1")
            return message
        # except:
        #     message = configure_texts.error()
        #     return message
    async def show_character(self, id):
        self.cur.execute("select characters.class, characters.name, characters.exp, characters.exp_next_lvl, "
                         "characters.lvl, characters.strength, characters.agility, characters.intelligence,"
                         "inventory.weapon, inventory.head, inventory.body, inventory.hands, inventory.legs "
                         "from characters "
                         "join inventory on characters.inventory = inventory.player_id "
                         "where id = %s", (id))  # добавил characters.class
        char = self.cur.fetchone()
        message = configure_texts.characteristics(char[0], char[1], char[2], char[3],
                                                  char[4], char[5],
                                                  char[6], char[7],
                                                  char[8], char[9], char[10], char[11], char[12])  # добавил еще char
        return message
    async def load_characters(self):
        self.cur.execute("select characters.id, characters.name, characters.exp, characters.exp_next_lvl, "
                         "characters.lvl, characters.strength, characters.agility, characters.intelligence, characters.class, "
                         "inventory.weapon, inventory.head, inventory.body, inventory.hands, inventory.legs "
                         "from characters "
                         "join inventory on characters.inventory = inventory.player_id "
                         )
        chars = self.cur.fetchall()
        return chars
    async def get_monster(self):
        self.cur.execute("select monster from monsters order by rand() limit 1")
        monster = self.cur.fetchone()
        return monster
    async def delete_character(self, id):
        try:
            self.cur.execute("delete from characters where id = %s", (id))
            self.cur.execute("delete from inventory where player_id = %s", (id))
            self.conn.commit()
            message = configure_texts.delete_character()
            return message
        except:
            message = configure_texts.error()
            return message
    async def add_item(self, item):
        self.cur.execute("insert into items(name, lvl, type, value) values (%s, %s, %s, %s)",
                         ("{} {}".format(item[0], item[1]), item[2], item[3], item[4]))
        self.conn.commit()
    def close(self):
        self.conn.close()