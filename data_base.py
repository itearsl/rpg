import pymysql
import configure_texts





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
        try:
            self.cur.execute("insert into characters values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (
                           id, character.name, character.exp, character.exp_next_lvl, character.lvl, character.strength,
                           character.agility, character.intelligence, id, character.specialist, character.money))
            self.cur.execute('insert into inventory values(%s,"кинжал-2","пусто-0","порваная накидка-2","пусто-0","лапти-1")',
                             (id))
            self.conn.commit()
            message = configure_texts.characteristics(character.specialist ,character.name, character.exp, character.exp_next_lvl,
                                                      character.lvl, character.strength,
                                                      character.agility, character.intelligence,
                                                      "кинжал-2", "пусто-0", "порваная накидка-2", "пусто-0", "лапти-1")
            return message
        except:
            message = configure_texts.error()
            return message
    async def show_character(self, id):
        self.cur.execute("select characters.name, characters.exp, characters.exp_next_lvl, "
                         "characters.lvl, characters.strength, characters.agility, characters.intelligence,"
                         "inventory.weapon, inventory.head, inventory.body, inventory.hands, inventory.legs, characters.class "
                         "from characters "
                         "join inventory on characters.inventory = inventory.player_id "
                         "where id = %s", (id))
        char = self.cur.fetchone()
        message = configure_texts.characteristics(char[12], char[0], char[1], char[2],
                                                  char[3], char[4],
                                                  char[5], char[6],
                                                  char[7], char[8], char[9], char[10], char[11])
        return message
    async def load_characters(self):
        self.cur.execute("select characters.id, characters.name, characters.exp, characters.exp_next_lvl, "
                         "characters.lvl, characters.strength, characters.agility, characters.intelligence, characters.class, "
                         "inventory.weapon, inventory.head, inventory.body, inventory.hands, inventory.legs, "
                         "characters.money "
                         "from characters "
                         "join inventory on characters.inventory = inventory.player_id "
                         )
        chars = self.cur.fetchall()
        return chars
    def save_characters(self, hero, id):
        self.cur.execute("update characters set exp = %s where id = %s", (hero.exp, id))
        self.cur.execute("update characters set exp_next_lvl = %s where id = %s", (hero.exp_next_lvl, id))
        self.cur.execute("update characters set lvl = %s where id = %s", (hero.lvl, id))
        self.cur.execute("update characters set strength = %s where id = %s", (hero.strength, id))
        self.cur.execute("update characters set intelligence = %s where id = %s", (hero.intelligence, id))
        self.cur.execute("update characters set agility = %s where id = %s", (hero.agility, id))
        self.cur.execute("update characters set money = %s where id = %s", (hero.money, id))
        self.conn.commit()
    async def get_monster(self, current_location):
        self.cur.execute("select monster from monsters "
                         "where location = 'Все' or location = %s"
                         "order by rand() limit 1", (current_location))
        monster = self.cur.fetchone()
        return monster
    async def get_locations(self):
        self.cur.execute("select location from locations order by rand() limit 3")
        locations = self.cur.fetchall()
        return locations
    async def get_desc(self, location):
        self.cur.execute("select descr from locations "
                         "where location = %s", (location))
        desc = self.cur.fetchone()
        return desc
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
    async def get_equip(self, part, id):
        task = "select {} from inventory where player_id = {}".format(part, id)
        self.cur.execute(task)
        equiped = self.cur.fetchone()
        return equiped
    async def change_equip(self, id, equip):
        task = "update inventory set {} = '{}-{}' " \
               "where player_id = {}".format(equip[1], equip[0], equip[2], id)
        self.cur.execute(task)
        self.conn.commit()
    async def get_item(self, lvl):
        self.cur.execute("select name, type, value, lvl from items "
                         "where lvl <= %s "
                         "order by rand() limit 1",(lvl))
        item = self.cur.fetchone()
        return item
    def close(self):
        self.conn.close()