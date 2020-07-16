from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class KB():

    async def travel_keyboard(self, locations):
        travel_keyboard = VkKeyboard(one_time=False, inline=True)
        for location in locations:
            travel_keyboard.add_button(location[0], VkKeyboardColor.DEFAULT)
            # travel_keyboard.add_line()
        return travel_keyboard