from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text

# from app.handlers.ticket_buying import OrderTicket


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # buttons = [
    #     types.InlineKeyboardButton(text="Группа вк", url="https://vk.com/vzpkk"),
    #     types.InlineKeyboardButton(text="Купить билет", callback_data="buying_ticket"),
    #     types.InlineKeyboardButton(text="Купить мерч", callback_data="buying_merch")
    # ]
    buttons = ["Узнать информацию!", "Купить билет!", "Купить мерч!"]
    keyboard.add(*buttons)
    await message.answer("Приветствую тебя в боте Взрывпакека!\n"
                         "Чем могу быть полезен?", reply_markup=keyboard)


# async def start_ticket_callback(call: types.CallbackQuery, state: FSMContext):
#     await call.message.answer("Секундочку...")
#     # await state.set_state(OrderTicket.starting_buying.state)


def register_handlers_starting(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    # dp.register_callback_query_handler(start_ticket_callback, Text(equals="buying_ticket"))
