from os import getenv
import logging
from consts import *
from user import *
from utils import MyStates
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="show")
async def show(message: types.Message):
    uid = message.from_user.id
    if uid in users:
        user = users[uid]
        await message.answer(MESSAGES["show_info"].format(user.fname, user.sname, user.age))
    else:
        await message.answer(MESSAGES["no_user"])

@dp.message_handler(commands="save_my_date")
async def save_my_date(message: types.Message):
    await message.answer(MESSAGES["save"])
    uid = message.from_user.id
    if uid not in users:
        user = User(uid)
        users[uid] = user
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(MyStates.WAITING_FIRST_NAME[0])

@dp.message_handler(state=MyStates.WAITING_FIRST_NAME)
async def first_test_state_case_met(message: types.Message):
    user = users[message.from_user.id]
    user.fname = message.text
    await message.answer(MESSAGES["wait_sn"].format(user.fname))
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(MyStates.WAITING_SECOND_NAME[0])

@dp.message_handler(state=MyStates.WAITING_SECOND_NAME)
async def second_test_state_case_met(message: types.Message):
    user = users[message.from_user.id]
    user.sname = message.text
    await message.answer(MESSAGES["wait_age"].format(user.fname, user.sname))
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(MyStates.WAITING_AGE[0])

@dp.message_handler(state=MyStates.WAITING_AGE)
async def age_test_state_case_met(message: types.Message):
    try:
        user = users[message.from_user.id]
        age = int(message.text)
        if age < 0 or age > 200:
            raise Exception
        user.age = age
        await message.answer(MESSAGES["all"])
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state(True)
    except:
        await message.answer(MESSAGES["error_age"])



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)