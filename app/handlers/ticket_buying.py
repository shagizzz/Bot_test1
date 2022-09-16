from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

available_tickets = ['Стандартный = 1500 р.', "Ягермейстер-билет = 1300 р."]


class OrderTicket(StatesGroup):
    starting_buying = State()
    waiting_for_ticket = State()
    waiting_for_fio = State()
    waiting_for_age = State()
    waiting_for_kurs = State()


async def ticket_starting(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in available_tickets:
        keyboard.add(name)
    await message.answer("Выберите билет", reply_markup=keyboard)
    await state.set_state(OrderTicket.waiting_for_ticket.state)


async def ticket_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_tickets:
        await message.answer("Пожалуйста, выберите из существующих билетов :)")
        return

    await state.update_data(chosen_ticket=message.text.lower())

    await state.set_state(OrderTicket.waiting_for_fio.state)
    await message.answer("Введите, пожалуйста, свое ФИО", reply_markup=types.ReplyKeyboardRemove())


async def getting_fio(message: types.Message, state: FSMContext):
    if len(message.text.split()) < 2:
        await message.answer("Введите, пожалуйста, хотя бы имя и фамилию! Это нужно для проверки оплаты :)")
        return
    await state.update_data(client_fio=message.text)

    await state.set_state(OrderTicket.waiting_for_age.state)
    await message.answer("Введите свой возраст, пожалуйста :)")


async def getting_age(message: types.Message, state: FSMContext):
    if int(message.text) < 18 or int(message.text) > 50:
        await message.answer("Если вам меньше 18 лет, мы, к сожалению, должны вам отказать :( \n"
                             "Если же Вам больше 50, то делать Вам на Взрывпакеке нечего :) \n"
                             "Если хотите поменять, указанный возраст, нажмите кнопку ниже:")
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Меняем возраст!")
        keyboard.add(button)
        await message.answer("ММммм???", reply_markup=keyboard)
        return
    await state.update_data(client_age=message.text)

    await state.set_state(OrderTicket.waiting_for_kurs.state)
    await message.answer("Введите, на каком курсе Вы учитесь в данный момент. \n"
                         "Если же Вы выпускник или в академическом отпуске, укажите это.")


async def getting_kurs(message: types.Message, state: FSMContext):
    await state.update_data(client_kurs=message.text)

    client_data = await state.get_data()
    await message.answer(f"Проверьте свои данные, все ли верно? \n"
                         f"Вас зовут: {client_data['client_fio']} \n"
                         f"Ваш возраст: {client_data['client_age']} \n"
                         f"Ваш курс: {client_data['client_kurs']} \n"
                         f"И Вы хотите купить билет: {client_data['chosen_ticket']}")
    await state.finish()


#
def register_ticket_buying_handler(dp: Dispatcher):
    dp.register_message_handler(ticket_starting, Text(equals="Купить билет!"), commands='ticket', state="*")
    dp.register_message_handler(ticket_chosen, state=OrderTicket.waiting_for_ticket)
    dp.register_message_handler(getting_fio, state=OrderTicket.waiting_for_fio)
    dp.register_message_handler(getting_age, state=OrderTicket.waiting_for_age)
    dp.register_message_handler(getting_kurs, state=OrderTicket.waiting_for_kurs)
