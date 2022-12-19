import sqlite3
import datetime

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def check_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, firstname, number, car_type, username):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (user_id, username, firstname, number, car_type) "
                                       "VALUES (?, ?, ?, ?, ?)", (user_id, username, firstname, number, car_type))

    def get_user_data(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE user_id = ?", (user_id,)).fetchall()
            return result[0][1:]

    def get_referal_points(self):
        with self.connection:
            result = self.cursor.execute("SELECT referal_points FROM `admin`").fetchone()
            return result[0]

    def get_km_points(self):
        with self.connection:
            result = self.cursor.execute("SELECT kilometrs_points FROM `admin`").fetchone()
            return result[0]

    def get_lite_km(self):
        with self.connection:
            result = self.cursor.execute("SELECT lightcar_kilometrs FROM `admin`").fetchone()
            return result[0]

    def get_hard_km(self):
        with self.connection:
            result = self.cursor.execute("SELECT hardcar_kilometrs FROM `admin`").fetchone()
            return result[0]

    def get_user_points(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT points FROM `users` WHERE user_id = ?", (user_id,)).fetchone()
            return result[0]

    def change_user_points(self, user_id, points):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET points = ? WHERE user_id =?", (points, user_id))

    def get_user_refs(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT referals FROM `users` WHERE user_id = ?", (user_id,)).fetchone()
            return result[0]

    def change_user_refs(self, user_id, points):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET referals = ? WHERE user_id =?", (points, user_id))

    def get_shop_values(self):
        with self.connection:
            values = self.cursor.execute("SELECT gods, price FROM `shop`").fetchall()
            return values

    def get_shop_names(self):
        with self.connection:
            names = self.cursor.execute("SELECT gods FROM `shop`").fetchall()
            result = [i[0] for i in names]
            return result

    def get_shop_price(self, name):
        with self.connection:
            result = self.cursor.execute("SELECT price FROM `shop` WHERE gods = ?", (name,)).fetchone()
            return result[0]

    def set_ref_points(self, points):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET referal_points = ?", (points,))

    def set_kil_points(self, points):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET kilometrs_points = ?", (points,))

    def set_lite_km(self, value):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET lightcar_kilometrs = ?", (value,))

    def set_hard_km(self, value):
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET hardcar_kilometrs = ?", (value,))

    def get_photo_link(self, name):
        with self.connection:
            result = self.cursor.execute("SELECT link FROM `photos` WHERE name = ?", (name,)).fetchone()
            return result

    def save_user_path(self, user_id, user_path):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET path = ? WHERE user_id =?", (user_path, user_id,))

    def get_car_type(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT car_type FROM `users` WHERE user_id = ?", (user_id,)).fetchone()[0]

    def export_to_exel(self):
        date = datetime.date.today()
        filename = f'{date.strftime("%d-%m-%Y")}.csv'
        with self.connection:
            with open(filename, 'w+') as write_file:
                for row in self.cursor.execute("SELECT * FROM `users`"):
                    new_row = ';'.join([str(x) for x in row])
                    write_file.write(new_row + '\n')
        return filename
