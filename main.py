import telebot
from telebot import apihelper
from db import Database
from location import Location
from utils import get_config, save_config
import keyboards

bot_username = 'squalor_bot'
config_filename = "config.json"
config = get_config(config_filename)
apihelper.ENABLE_MIDDLEWARE = True
db_file = config['database']
bot = telebot.TeleBot(config['bot_token'], parse_mode='HTML')
db = Database(db_file)
location = Location(telebot.TeleBot(config['bot_token'], parse_mode='HTML'), db_file)


def is_subscribed(user_id):
    arg = sub_channels(user_id)
    for channel_id in arg.values():
        chat_member = bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if chat_member.status == 'left':
            return False
    return True

def sub_channels(user_id):
    channels = {**config["channels"]}
    dict_one = channels.copy()
    for channel in dict_one:
        chat_member = bot.get_chat_member(chat_id=channels.get(channel), user_id=user_id)
        if chat_member.status != 'left':
            del channels[channel]
    return channels

@bot.message_handler(commands=['start'])
def start_message(message):
    args = message.text.split(' ')[1:]
    if db.check_user(message.from_user.id):
        bot.send_message(
            message.chat.id,
            text=config['text']['olduser'],
            reply_markup=keyboards.start_menu()
        )
    else:
        if len(args) < 1:
            bot.send_message(
                message.from_user.id,
                text=config['text']['newuser'],
                reply_markup=keyboards.opros()
            )
        else:
            new_points = db.get_user_points(args[0]) + db.get_referal_points()
            new_refs = db.get_user_refs(args[0]) + 1
            db.change_user_points(args[0], new_points)
            db.change_user_refs(args[0], new_refs)
            bot.send_message(
                message.from_user.id,
                text=config['text']['newuser'],
                reply_markup=keyboards.opros()
            )

@bot.message_handler(commands=['change_referal_points'])
def change_referal_points(message):
    args = message.text.split(' ')[1:]
    if len(args) < 1:
        bot.send_message(message.chat.id, text=config['text']['error'])
    else:
        try:
            new = int(args[0])
            db.set_ref_points(new)
            bot.send_message(message.chat.id, text=config['text']['complete'])
        except ValueError:
            bot.send_message(message.chat.id, text=config['text']['error'])

@bot.message_handler(commands=['change_main_points'])
def change_main_points(message):
    args = message.text.split(' ')[1:]
    if len(args) < 1:
        bot.send_message(message.chat.id, text=config['text']['error'])
    else:
        try:
            new = int(args[0])
            db.set_kil_points(new)
            bot.send_message(message.chat.id, text=config['text']['complete'])
        except ValueError:
            bot.send_message(message.chat.id, text=config['text']['error'])

@bot.message_handler(commands=['change_lite_km'])
def change_lite_km(message):
    args = message.text.split(' ')[1:]
    if len(args) < 1:
        bot.send_message(message.chat.id, text=config['text']['error'])
    else:
        try:
            new = int(args[0])
            db.set_lite_km(new)
            bot.send_message(message.chat.id, text=config['text']['complete'])
        except ValueError:
            bot.send_message(message.chat.id, text=config['text']['error'])

@bot.message_handler(commands=['export'])
def change_lite_km(message):
    bot.send_chat_action(message.chat.id, action='typing', timeout=3)
    bot.send_document(message.chat.id, open(db.export_to_exel(), 'rb'))


@bot.message_handler(commands=['change_hard_km'])
def change_lite_km(message):
    args = message.text.split(' ')[1:]
    if len(args) < 1:
        bot.send_message(message.chat.id, text=config['text']['error'])
    else:
        try:
            new = int(args[0])
            db.set_hard_km(new)
            bot.send_message(message.chat.id, text=config['text']['complete'])
        except ValueError:
            bot.send_message(message.chat.id, text=config['text']['error'])

@bot.message_handler(commands=['get_values'])
def get_values(message):
    ref_points = db.get_referal_points()
    km_points = db.get_km_points()
    lite_km = db.get_lite_km()
    hard_km = db.get_hard_km()
    bot.send_message(message.chat.id, text=config['text']['get_values'].format(ref_points, km_points, lite_km, km_points, hard_km))

@bot.middleware_handler(update_types=['edited_message'])
def edited_message(bot_instanse, message):
    user_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude
    live_period = message.location.live_period
    loc = (latitude, longitude)
    location.main_theam(user_id, loc, live_period)



@bot.message_handler(content_types=['text'])
def user_message(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(
            message.from_user.id,
            text=config['text']['sub_channel'],
            reply_markup=keyboards.sub_channel(sub_channels(message.from_user.id))
        )
        return
    if message.text == 'Личный кабинет':
        sub_channels(message.from_user.id)
        userdata = db.get_user_data(message.from_user.id)
        bot.send_message(
            message.chat.id,
            text=config['text']['cabinet'].format(userdata[0], userdata[1], userdata[2], userdata[3],
                                                  userdata[4], userdata[5], userdata[6])
        )
    elif message.text == 'Получить реферальную ссылку':
        bot.send_message(message.from_user.id, text=config['text']['ref_link'].format(bot_name=bot_username,
                                                                                      user_id=message.from_user.id))
    elif message.text == 'Магазин':
        values = db.get_shop_values()
        bot.send_message(message.from_user.id, text=config['text']['shop'], reply_markup=keyboards.shop(values))
    elif message.text == 'Начать поездку':
        bot.send_message(message.from_user.id, text='Инструкция по запуску транслирования геолокации')
        location.del_from_stop_list(message.from_user.id)

def get_number(message):
    number = message.contact.phone_number
    firstname = message.contact.first_name + ' '
    if not message.contact.last_name is None:
        firstname += message.contact.last_name
    msg = bot.send_message(
        message.chat.id,
        text=config['text']['choose_car'],
        reply_markup=keyboards.car_type()
    )
    bot.register_next_step_handler(msg, get_car, firstname=firstname, number=number)

def get_car(message,firstname, number):
    car_type = message.text
    msg = bot.send_message(
        message.chat.id,
        text=config['text']['allright'].format(firstname, number, car_type),
        reply_markup=keyboards.yes_no()
    )
    bot.register_next_step_handler(msg, get_answer, firstname, number, car_type)

def get_answer(message, firstname, number, car_type):
    if message.text == 'Верно':
        if message.from_user.username is None:
            username = 'default'
        else:
            username = message.from_user.username
        db.add_user(message.from_user.id, firstname, number, car_type, username)
        bot.send_message(message.chat.id,
                         text=config['text']['tnx'],
                         reply_markup=keyboards.start_menu())
    elif message.text == 'Не Верно':
        bot.send_message(message.chat.id,
                         text=config['text']['try_again'])
        bot.register_next_step_handler(message, get_number)

@bot.callback_query_handler(func=lambda c: True)
def callback_query(c):
    user_id = c.from_user.id
    if c.data == 'sub':
        if not is_subscribed(user_id):
            arg = sub_channels(user_id)
            bot.send_message(
                c.from_user.id,
                text=config['text']['sub_channel'],
                reply_markup=keyboards.sub_channel(arg)
            )
            return
        bot.send_message(
            c.from_user.id,
            text=config['text']['olduser'],
            reply_markup=keyboards.start_menu()
        )
    elif c.data == 'start_opros':
        bot.delete_message(c.from_user.id, c.message.message_id)
        msg = bot.send_message(
            c.from_user.id,
            text=config['text']['get_number'],
            reply_markup=keyboards.get_number()
        )
        bot.register_next_step_handler(msg, get_number)
    elif c.data in db.get_shop_names():
        photo = db.get_photo_link(c.data)
        price =db.get_shop_price(c.data)
        if photo is None:
            bot.delete_message(c.from_user.id, c.message.message_id)
            bot.send_message(c.from_user.id, text=config['text'][c.data], reply_markup=keyboards.buy(c.data, price))
        else:
            bot.delete_message(c.from_user.id, c.message.message_id)
            bot.send_photo(c.from_user.id, open(photo[0], 'rb'), caption=config['text'][c.data], reply_markup=keyboards.buy(c.data, price))

    elif c.data.startswith('buy'):
        name = c.data.split('_')[1]
        if db.get_shop_price(name) <= db.get_user_points(c.from_user.id):
            bot.delete_message(c.from_user.id, c.message.message_id)
            new_points = db.get_user_points(c.from_user.id) - db.get_shop_price(name)
            db.change_user_points(c.from_user.id, new_points)
            bot.delete_message(c.from_user.id, c.message.message_id)
            bot.send_message(c.from_user.id, text=config['text']['tnx_for_buying'].format(name,
                                                                                          db.get_shop_price(c.data)))
            bot.send_message(config['admin'], text=config['text']['shop_notification'].format(c.from_user.username,
                                                                                              c.from_user.id, name,
                                                                                              db.get_shop_price(
                                                                                                  name)))
        else:
            bot.delete_message(c.from_user.id, c.message.message_id)
            bot.send_message(c.from_user.id, text=config['text']['no_money'])

    elif c.data == 'back':
        values = db.get_shop_values()
        bot.delete_message(c.from_user.id, c.message.message_id)
        bot.send_message(c.from_user.id, text=config['text']['shop'], reply_markup=keyboards.shop(values))
    elif c.data == 'stop':
        location.add_to_stop_list(c.from_user.id)
        bot.send_message(c.from_user.id, text='Через пять минут вы заверите поездку, спасибо!')
    elif c.data == 'cont':
        location.del_from_stop_list(c.from_user.id)
        bot.send_message(c.from_user.id, text='Поездка продолжается!')

if __name__ == '__main__':
    bot.polling(non_stop=True)



"""        if db.get_shop_price(c.data) <= db.get_user_points(c.from_user.id):
            bot.delete_message(c.from_user.id, c.message.message_id)
            new_points = db.get_user_points(c.from_user.id) - db.get_shop_price(c.data)
            db.change_user_points(c.from_user.id, new_points)
            bot.send_message(c.from_user.id, text=config['text']['tnx_for_buying'].format(c.data,
                                                                                          db.get_shop_price(c.data)))
            bot.send_message(config['admin'], text=config['text']['shop_notification'].format(c.from_user.username,
                                                                                              c.from_user.id, c.data,
                                                                                              db.get_shop_price(c.data)))
        else:
            bot.delete_message(c.from_user.id, c.message.message_id)
            bot.send_message(c.from_user.id, text=config['text']['no_money'])
"""