import telebot
from db import Database
from time import sleep
from math import *
from threading import Thread

import telebot.apihelper


class Location:
    def __init__(self, bot, db_file):
        self.bot = bot
        self.db = Database(db_file)
        self.sleepers = set()
        self.workers = set()
        self.stop_list = set()
        self.locations = dict()

    def add_to_sleep(self, user_id: int):
        self.sleepers.add(user_id)
        sleep(60)
        self.sleepers.discard(user_id)

    def four_hours(self, user_id, live_period, continue_work=False):
        self.workers.add(user_id)
        markup = telebot.types.InlineKeyboardMarkup()
        k1 = telebot.types.InlineKeyboardButton(text='Продолжить', callback_data='cont')
        k2 = telebot.types.InlineKeyboardButton(text='Завершить', callback_data='stop')
        markup.row(k1, k2)
        if live_period > 3600:
            sleep(14100)
            # Бот отправляет напоминиание пользователю
            self.bot.send_message(user_id, text='До завершения логирования осталось 5 минут. '
                                                'вы хотите продолжить поездку?', reply_markup=markup)
            sleep(300)
            user_path = self.send_location(user_id)
            # Бот выводит информацию пользователю
            self.bot.send_message(user_id, text=f'Поездка завершена, вы проехали ~{user_path} м.', reply_markup=markup)
            # Бот сохраняет информацию в БД
            user_points = 0
            if self.db.get_car_type(user_id) == 'Легковой':
                user_points = self.db.get_user_points(user_id) + int(user_path / 10)
                #user_points = self.db.get_user_points(user_id) + (user_path / 1000 / self.db.get_lite_km() * self.db.get_km_points())
            elif self.db.get_car_type(user_id) == 'Грузовой':
                user_points = self.db.get_user_points(user_id) + int(user_path / 10)
                #user_points = self.db.get_user_points(user_id) + (user_path / 1000 / self.db.get_hard_km() * self.db.get_km_points())
            self.db.change_user_points(user_id, user_points)
            self.workers.discard(user_id)
        else:
            sleep(live_period - 300)
            # Бот отправляет напоминиание пользователю
            self.bot.send_message(user_id, text='До завершения логирования осталось 5 минут. '
                                                'вы хотите продолжить поездку?', reply_markup=markup)
            sleep(300)
            user_path = self.send_location(user_id)
            # Бот выводит информацию пользователю
            self.bot.send_message(user_id, text=f'Поездка завершена, вы проехали ~{user_path} м.')
            # Бот сохраняет информацию в БД
            user_points = 0
            if self.db.get_car_type(user_id) == 'Легковой':
                user_points = self.db.get_user_points(user_id) + int(user_path / 10)
                # user_points = self.db.get_user_points(user_id) + (user_path / 1000 / self.db.get_lite_km() * self.db.get_km_points())
            elif self.db.get_car_type(user_id) == 'Грузовой':
                user_points = self.db.get_user_points(user_id) + int(user_path / 10)
                # user_points = self.db.get_user_points(user_id) + (user_path / 1000 / self.db.get_hard_km() * self.db.get_km_points())
            self.db.change_user_points(user_id, user_points)
            self.workers.discard(user_id)

    def get_distance(self, location1: tuple = ('latitude', 'longetude'), location2: tuple = ('latitude', 'longetude')):
        lat1, lon1 = location1
        lat2, lon2 = location2
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        path = 6371 * c * 1000
        return int(path)

    def main_theam(self, user_id, location, live_period):
        if user_id not in self.stop_list:
            if user_id not in self.workers and user_id not in self.sleepers:
                worker = Thread(target=self.four_hours, args=(user_id, live_period))
                sleeper = Thread(target=self.add_to_sleep, args=(user_id,))
                worker.start()
                sleeper.start()
                self.locations[user_id] = dict()
                self.locations[user_id][len(self.locations[user_id]) + 1] = location
            elif user_id in self.workers and user_id not in self.sleepers:
                sleeper = Thread(target=self.add_to_sleep, args=(user_id,))
                sleeper.start()
                self.locations[user_id][len(self.locations[user_id]) + 1] = location
        else:
            self.bot.send_message(user_id, text='Для того чтобы начать логирование расстояний нажмите'
                                                ' "Начтать поездку" в главном меню')

    def send_location(self, user_id):
        user_path = 0
        for x in range(1, len(self.locations[user_id])):
                y = x + 1
                user_path += self.get_distance(self.locations[user_id][x], self.locations[user_id][y])
        return user_path

    def add_to_stop_list(self, user_id):
        sleep(240)
        self.stop_list.add(user_id)

    def del_from_stop_list(self, user_id):
        self.stop_list.discard(user_id)
