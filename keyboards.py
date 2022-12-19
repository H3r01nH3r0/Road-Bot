from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

def start_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton(text='Начать поездку'))
    markup.row(KeyboardButton(text='Личный кабинет'), KeyboardButton(text='Получить реферальную ссылку'))
    markup.row(KeyboardButton(text='Магазин'))
    return markup

def car_type():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton(text='Легковой'), KeyboardButton(text='Грузовой'))
    return markup

def yes_no():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton(text='Верно'), KeyboardButton(text='Не Верно'))
    return markup

def sub_channel(channels: dict) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for i, channel_url in enumerate(channels.keys(), start=1):
        markup.add(InlineKeyboardButton(text='Подписаться', url=channel_url))
    markup.add(InlineKeyboardButton(text='Проверить', callback_data="sub"))
    return markup

def opros():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Пройти верификацию', callback_data='start_opros'))
    return markup

def shop(vauels):
    markup = InlineKeyboardMarkup()
    for name, price in vauels:
        markup.add(InlineKeyboardButton(text=f'{name}', callback_data=name))
    return markup

def get_number():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(text="Поделиться контактом", request_contact=True))
    return markup

def buy(name, price):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f'Купить | {price} баллов', callback_data='buy_' + name))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    return markup