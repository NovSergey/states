from aiogram.utils.helper import Helper, HelperMode, ListItem


class MyStates(Helper):
    mode = HelperMode.snake_case

    WAITING_FIRST_NAME = ListItem()
    WAITING_SECOND_NAME = ListItem()
    WAITING_AGE = ListItem()