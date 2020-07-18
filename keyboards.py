from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class KB():

    def __init__(self):
        self.__choice_keyboard = VkKeyboard(inline=True)
        self.__choice_keyboard.add_button("Вернуться в Дрифтвуд", VkKeyboardColor.POSITIVE)
        self.__choice_keyboard.add_line()
        self.__choice_keyboard.add_button("Путешествие", VkKeyboardColor.POSITIVE)
        self.__choice_keyboard.add_line()
        self.__choice_keyboard.add_button("Охота", VkKeyboardColor.NEGATIVE)

        self.__town_keyboard = VkKeyboard(inline=True)
        self.__town_keyboard.add_button("Путешествие", VkKeyboardColor.POSITIVE)
        self.__town_keyboard.add_line()
        self.__town_keyboard.add_button("Магазин", VkKeyboardColor.POSITIVE)

    @property
    def choice_keyboard(self):
        return self.__choice_keyboard

    @property
    def town_keyboard(self):
        return self.__town_keyboard

    async def travel_keyboard(self, locations):
        travel_keyboard = VkKeyboard(inline=True)
        for i, location in enumerate(locations):
            travel_keyboard.add_button(location[0], VkKeyboardColor.POSITIVE)
            if i != 2:
                travel_keyboard.add_line()
        return travel_keyboard

    async def fight_keyboard(self, character):
        fight_keyboard = VkKeyboard(inline=True)
        fight_keyboard.add_button("Удар", VkKeyboardColor.NEGATIVE)
        if character.specialist == "Warrior":
            fight_keyboard.add_line()
            fight_keyboard.add_button("Сильный Удар", VkKeyboardColor.NEGATIVE)
            return fight_keyboard
        elif character.specialist == "Mage":
            fight_keyboard.add_line()
            fight_keyboard.add_button("Огненный шар", VkKeyboardColor.NEGATIVE)
            return fight_keyboard
        elif character.specialist == "Rogue":
            fight_keyboard.add_line()
            fight_keyboard.add_button("Удар в спину", VkKeyboardColor.NEGATIVE)
            return fight_keyboard
