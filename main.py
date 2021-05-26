
import datetime
import sys
from os.path import exists
from content import User
from content import Route
import content

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLineEdit, QLabel)



class Program(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 200)
        self.setWindowTitle('Start')

        self.hello_label = QLabel(self)
        self.hello_label.setText("Hello bike-trips stats system")
        self.hello_label.move(120, 50)
        self.hello_label.show()

        self.hello_btn1 = QPushButton(self)
        self.hello_btn1.setText("Add user")
        self.hello_btn1.move(150, 100)
        self.hello_btn1.show()
        self.hello_btn1.clicked.connect(self.add_user)

        self.hello_btn2 = QPushButton(self)
        self.hello_btn2.setText("Log in")
        self.hello_btn2.move(150, 130)
        self.hello_btn2.show()
        self.hello_btn2.clicked.connect(self.log_in)

        self.hello_btn3 = QPushButton(self)
        self.hello_btn3.setText("Exit")
        self.hello_btn3.move(150, 160)
        self.hello_btn3.show()
        self.hello_btn3.clicked.connect(QCoreApplication.instance().quit)

        self.show()

    def add_user(self):
        self.add = Add_User()
        self.close()

    def log_in(self):
        self.log = Log_In()
        self.close()


class Add_User(QWidget):
    def __init__(self):
        super().__init__()
        self.add_us()

    def add_us(self):
        self.resize(400, 200)
        self.setWindowTitle('Add user')

        self.label = QLabel(self)
        self.label.setText("Input user name")
        self.label.move(50, 10)
        self.label.show()

        self.name = QLineEdit(self)
        self.name.move(140, 10)
        self.name.show()

        self.label1 = QLabel(self)
        self.label1.setText("Input birth year: ")
        self.label1.move(50, 40)
        self.label1.show()

        self.year = QLineEdit(self)
        self.year.move(140, 40)
        self.year.show()

        self.label2 = QLabel(self)
        self.label2.setText("Input birth month: ")
        self.label2.move(50, 70)
        self.label2.show()

        self.month = QLineEdit(self)
        self.month.move(140, 70)
        self.month.show()

        self.label3 = QLabel(self)
        self.label3.setText("Input birth day: ")
        self.label3.move(50, 100)
        self.label3.show()

        self.day = QLineEdit(self)
        self.day.move(140, 100)
        self.day.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Next")
        self.btn1.move(150, 140)
        self.btn1.show()
        self.btn1.clicked.connect(self.next)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Cancel")
        self.btn2.move(150, 170)
        self.btn2.show()
        self.btn2.clicked.connect(self.cancel)

        self.show()

    def next(self):
        file = str(self.name.text()) + ".txt"
        print(file)
        if not exists(file):
            try:
                d = datetime.date(int(self.year.text()), int(self.month.text()), int(self.day.text()))
                print(d)
                if d > datetime.date.today():
                    self.wr = Wrong_date()
                else:
                    us = User(str(self.name.text()), str(self.day.text()), str(self.month.text()),
                              str(self.year.text()))
                    us.save_stats()
                    self.p = Program()
                    self.close()
            except ValueError:
                self.wr = Wrong_date()

        else:
            self.al = User_already_exists()

    def cancel(self):
        self.p = Program()
        self.close()


class User_already_exists(QWidget):
    def __init__(self):
        super().__init__()
        self.message()

    def message(self):
        self.resize(150, 100)
        self.setWindowTitle('Add user')

        self.mes = QLabel(self)
        self.mes.setText("This user already exists!")
        self.mes.move(10, 30)
        self.mes.show()

        self.btn = QPushButton(self)
        self.btn.setText("OK")
        self.btn.move(30, 60)
        self.btn.show()
        self.btn.clicked.connect(self.c)

        self.show()

    def c(self):
        self.close()


class Wrong_date(QWidget):
    def __init__(self):
        super().__init__()
        self.message()

    def message(self):
        self.resize(100, 100)
        self.setWindowTitle('Add user')

        self.mes = QLabel(self)
        self.mes.setText("Wrong date!")
        self.mes.move(10, 30)
        self.mes.show()

        self.btn = QPushButton(self)
        self.btn.setText("OK")
        self.btn.move(30, 60)
        self.btn.show()
        self.btn.clicked.connect(self.c)

        self.show()

    def c(self):
        self.close()


class Log_In(QWidget):
    def __init__(self):
        super().__init__()
        self.log_in()

    def log_in(self):
        self.resize(400, 200)
        self.setWindowTitle('Log in')

        self.label = QLabel(self)
        self.label.setText("Input user name")
        self.label.move(50, 80)
        self.label.show()

        self.name = QLineEdit(self)
        self.name.move(140, 80)
        self.name.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Next")
        self.btn1.move(150, 140)
        self.btn1.show()
        self.btn1.clicked.connect(self.next)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Cancel")
        self.btn2.move(150, 170)
        self.btn2.show()
        self.btn2.clicked.connect(self.cancel)

        self.show()

    def next(self):
        file = str(self.name.text()) + ".txt"
        print(file)
        if exists(file):
            current_user = self.get_user(self.name.text())
            current_user.get_routes()
            self.main_win = MainWindow(current_user)
            self.close()

        else:
            self.al = User_Doesnt_Exist()

    def cancel(self):
        self.p = Program()
        self.close()

    def get_user(self, name):
        file = str(name) + ".txt"
        with open(file, encoding="utf8") as f:
            table = f.readline().split("\t")
            return User(table[0], table[1], table[2], table[3])


class User_Doesnt_Exist(QWidget):
    def __init__(self):
        super().__init__()
        self.message()

    def message(self):
        self.resize(100, 100)
        self.setWindowTitle('Log In')

        self.mes = QLabel(self)
        self.mes.setText("User doesn't exist!")
        self.mes.move(10, 30)
        self.mes.show()

        self.btn = QPushButton(self)
        self.btn.setText("OK")
        self.btn.move(30, 60)
        self.btn.show()
        self.btn.clicked.connect(self.c)

        self.show()

    def c(self):
        self.close()


class MainWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.w()

    def w(self):
        self.resize(400, 250)
        self.setWindowTitle('Start')

        self.hello_label = QLabel(self)
        self.hello_label.setText("What would you want to do?")
        self.hello_label.move(120, 10)
        self.hello_label.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Show my routes")
        self.btn1.move(100, 40)
        self.btn1.resize(200, 20)
        self.btn1.show()
        self.btn1.clicked.connect(self.sh_my_routes)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Show all the routes I have access for")
        self.btn2.move(100, 70)
        self.btn2.resize(200, 20)
        self.btn2.show()
        self.btn2.clicked.connect(self.sh_all_routes)

        self.btn3 = QPushButton(self)
        self.btn3.setText("Show specific stats")
        self.btn3.move(100, 100)
        self.btn3.resize(200, 20)
        self.btn3.show()
        self.btn3.clicked.connect(self.sh_spec_stats)

        self.btn4 = QPushButton(self)
        self.btn4.setText("Find route by name")
        self.btn4.move(100, 130)
        self.btn4.resize(200, 20)
        self.btn4.show()
        self.btn4.clicked.connect(self.find_route)

        self.btn5 = QPushButton(self)
        self.btn5.setText("Add new route")
        self.btn5.move(100, 160)
        self.btn5.resize(200, 20)
        self.btn5.show()
        self.btn5.clicked.connect(self.add_r)

        self.btn6 = QPushButton(self)
        self.btn6.setText("Send all my routes to another user")
        self.btn6.move(100, 190)
        self.btn6.resize(200, 20)
        self.btn6.show()
        self.btn6.clicked.connect(self.add_f)

        self.btn7 = QPushButton(self)
        self.btn7.setText("Log out")
        self.btn7.move(100, 220)
        self.btn7.resize(200, 20)
        self.btn7.show()
        self.btn7.clicked.connect(self.logout)

        self.show()

    def sh_my_routes(self):
        self.h = My_Routes(self.user)

    def sh_all_routes(self):
        self.h = All_Routes(self.user)

    def sh_spec_stats(self):
        self.h = Spec_Routes(self.user)

    def find_route(self):
        self.a = Find(self.user)

    def add_r(self):
        self.a = Add_R(self.user)

    def add_f(self):
        self.a = Add_F(self.user)

    def logout(self):
        self.cl = Program()
        self.close()

    def get_user(self, name):
        file = str(name) + ".txt"
        with open(file, encoding="utf8") as f:
            table = f.readline().split("\t")
            return User(table[0], table[1], table[2], table[3])


class Add_R(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.message()

    def message(self):
        self.resize(400, 250)
        self.setWindowTitle('Add route')

        self.label = QLabel(self)
        self.label.setText("Input .gpx file")
        self.label.move(100, 40)
        self.label.show()

        self.label2 = QLabel(self)
        self.label2.setText("Input new name")
        self.label2.move(100, 70)
        self.label2.show()

        self.gpxfile = QLineEdit(self)
        self.gpxfile.move(200, 40)
        self.gpxfile.show()

        self.name = QLineEdit(self)
        self.name.move(200, 70)
        self.name.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Next")
        self.btn1.move(180, 140)
        self.btn1.show()
        self.btn1.clicked.connect(self.next)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Cancel")
        self.btn2.move(180, 170)
        self.btn2.show()
        self.btn2.clicked.connect(self.cancel)

        self.show()

        

    def next(self):
        if str(self.gpxfile.text())[-4:] != ".gpx":
            self.ex = Wrong_Gpx_File()
        elif not exists(str(self.gpxfile.text())):
            self.ex = File_NotExists()
        else:
            route_exists = False
            if len(self.user.my_routes) > 0:
                for r in self.user.my_routes:
                    if r.name == str(self.name.text()):
                        route_exists = True
            if route_exists:
                self.ex = Route_already_exists()
            else:
                new = self.user.add_route(str(self.name.text()), self.gpxfile.text())
                self.user.my_routes.append(new)
                self.user.save_stats()
                self.close()

    def cancel(self):
        self.close()


class File_NotExists(QWidget):
    def __init__(self):
        super().__init__()
        self.message()

    def message(self):
        self.resize(100, 100)
        self.setWindowTitle('Add route')

        self.mes = QLabel(self)
        self.mes.setText("File doesn't exist!")
        self.mes.move(10, 30)
        self.mes.show()

        self.btn = QPushButton(self)
        self.btn.setText("OK")
        self.btn.move(30, 60)
        self.btn.show()
        self.btn.clicked.connect(self.c)

        self.show()

    def c(self):
        self.close()


class Wrong_Gpx_File(QWidget):
    def __init__(self):
        super().__init__()
        self.message()

    def message(self):
        self.resize(100, 100)
        self.setWindowTitle('Add route')

        self.mes = QLabel(self)
        self.mes.setText("It's not a gpx file!")
        self.mes.move(10, 30)
        self.mes.show()

        self.btn = QPushButton(self)
        self.btn.setText("OK")
        self.btn.move(30, 60)
        self.btn.show()
        self.btn.clicked.connect(self.c)

        self.show()

    def c(self):
        self.close()


class Route_already_exists(QWidget):
    def __init__(self):
        super().__init__()
        self.message()

    def message(self):
        self.resize(100, 100)
        self.setWindowTitle('Add route')

        self.mes = QLabel(self)
        self.mes.setText("This file already exists!")
        self.mes.move(10, 30)
        self.mes.show()

        self.btn = QPushButton(self)
        self.btn.setText("OK")
        self.btn.move(30, 60)
        self.btn.show()
        self.btn.clicked.connect(self.c)

        self.show()

    def c(self):
        self.close()


class My_Routes(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.w()

    def w(self):
        self.resize(700, 200)
        self.setWindowTitle('My routes')

        self.label = QLabel(self)
        self.label.setText(self.user.__str__())
        self.label.move(250, 10)
        self.label.show()
        a = 50
        for i in self.user.my_routes:
            self.label = QLabel(self)
            self.label.setText(i.__str__())
            self.label.move(5, int(a))
            self.label.show()
            a += 20



        self.btn = QPushButton(self)
        self.btn.setText("Close")
        self.btn.move(330, 170)
        self.btn.show()
        self.btn.clicked.connect(self.cancel)

        self.show()


    def cancel(self):
        self.close()

    def get_user(self, name):
        file = str(name) + ".txt"
        with open(file, encoding="utf8") as f:
            table = f.readline().split("\t")
            return User(table[0], table[1], table[2], table[3])


class All_Routes(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.w()

    def w(self):
        self.resize(700, 200)
        self.setWindowTitle('All routes')

        self.label = QLabel(self)
        self.label.setText(self.user.__str__())
        self.label.move(250, 10)
        self.label.show()
        a = 50
        for i in self.user.my_routes:
            self.label = QLabel(self)
            self.label.setText(i.__str__())
            self.label.move(5, int(a))
            self.label.show()
            a += 20
        for i in self.user.friends_routes:
            self.label = QLabel(self)
            self.label.setText(i.__str__())
            self.label.move(5, int(a))
            self.label.show()
            a += 20



        self.btn = QPushButton(self)
        self.btn.setText("Close")
        self.btn.move(330, 170)
        self.btn.show()
        self.btn.clicked.connect(self.cancel)

        self.show()


    def cancel(self):
        self.close()


class Spec_Routes(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.w()

    def w(self):
        self.resize(700, 200)
        self.setWindowTitle('My routes')

        self.label = QLabel(self)
        self.label.setText(self.user.__str__())
        self.label.move(250, 10)
        self.label.show()
        a = 50
        for i in self.user.show_exclusive_stats():
            self.label = QLabel(self)
            self.label.setText(i.__str__())
            self.label.move(5, int(a))
            self.label.show()
            a += 20



        self.btn = QPushButton(self)
        self.btn.setText("Close")
        self.btn.move(330, 170)
        self.btn.show()
        self.btn.clicked.connect(self.cancel)

        self.show()


    def cancel(self):
        self.close()


class Add_F(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.w()

    def w(self):
        self.resize(400, 200)
        self.setWindowTitle('Send all Routes')

        self.label = QLabel(self)
        self.label.setText("Input user name")
        self.label.move(50, 80)
        self.label.show()

        self.name = QLineEdit(self)
        self.name.move(140, 80)
        self.name.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Next")
        self.btn1.move(150, 140)
        self.btn1.show()
        self.btn1.clicked.connect(self.next)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Cancel")
        self.btn2.move(150, 170)
        self.btn2.show()
        self.btn2.clicked.connect(self.cancel)

        self.show()

    def next(self):
        file = str(self.name.text()) + ".txt"
        if exists(file):
            current_user = self.get_user(self.name.text())
            current_user.get_routes()
            for r in self.user.my_routes:
                is_on_list = False
                for i in current_user.friends_routes:
                    if r.name == i.name and r.owner == i.owner:
                        is_on_list = True
                if not is_on_list:
                    current_user.friends_routes.append(r)
                    current_user.save_stats()
            self.close()

        else:
            self.al = User_Doesnt_Exist()

    def cancel(self):
        self.close()

    def get_user(self, name):
        file = str(name) + ".txt"
        with open(file, encoding="utf8") as f:
            table = f.readline().split("\t")
            return User(table[0], table[1], table[2], table[3])


class Find(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.w()

    def w(self):
        self.resize(400, 200)
        self.setWindowTitle('Find')

        self.label = QLabel(self)
        self.label.setText("Input Route name")
        self.label.move(50, 80)
        self.label.show()

        self.name = QLineEdit(self)
        self.name.move(140, 80)
        self.name.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Next")
        self.btn1.move(150, 140)
        self.btn1.show()
        self.btn1.clicked.connect(self.next)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Cancel")
        self.btn2.move(150, 170)
        self.btn2.show()
        self.btn2.clicked.connect(self.cancel)

        self.show()

    def next(self):
        r_found = False
        if len(self.user.my_routes) >0:

            for r in self.user.my_routes:
                if str(r.name) == str(self.name.text()):
                    r_found = True
                    self.ne = Route_Found(r)
        if not r_found:
            self.ex = Route_Doesnt_Exist()

    def cancel(self):
        self.close()


class Route_Doesnt_Exist(QWidget):
    def __init__(self):
        super().__init__()
        self.message()

    def message(self):
        self.resize(200, 100)
        self.setWindowTitle('Find route')

        self.mes = QLabel(self)
        self.mes.setText("There's no road with that name!")
        self.mes.move(30, 30)
        self.mes.show()

        self.btn = QPushButton(self)
        self.btn.setText("OK")
        self.btn.move(60, 60)
        self.btn.show()
        self.btn.clicked.connect(self.c)

        self.show()

    def c(self):
        self.close()


class Route_Found(QWidget):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.w()

    def w(self):
        self.resize(700, 100)
        self.setWindowTitle('Route')

        self.label = QLabel(self)
        self.label.setText(self.route.__str__())
        self.label.move(100, 10)
        self.label.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Send Route")
        self.btn1.move(300, 40)
        self.btn1.show()
        self.btn1.clicked.connect(self.next)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Close")
        self.btn2.move(300, 70)
        self.btn2.show()
        self.btn2.clicked.connect(self.cl)

        self.show()

    def next(self):
        self.ne = Choose_User(self.route)

    def cl(self):
        self.close()


class Choose_User(QWidget):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.w()

    def w(self):
        self.resize(400, 200)
        self.setWindowTitle('Send Route')

        self.label = QLabel(self)
        self.label.setText("Input user name")
        self.label.move(50, 80)
        self.label.show()

        self.name = QLineEdit(self)
        self.name.move(140, 80)
        self.name.show()

        self.btn1 = QPushButton(self)
        self.btn1.setText("Next")
        self.btn1.move(150, 140)
        self.btn1.show()
        self.btn1.clicked.connect(self.next)

        self.btn2 = QPushButton(self)
        self.btn2.setText("Cancel")
        self.btn2.move(150, 170)
        self.btn2.show()
        self.btn2.clicked.connect(self.cancel)

        self.show()

    def next(self):
        file = str(self.name.text()) + ".txt"
        if exists(file):
            current_user = self.get_user(self.name.text())
            current_user.get_routes()
            is_on_list = False
            for i in current_user.friends_routes:
                if self.route.name == i.name and self.route.owner == i.owner:
                    is_on_list = True
            if not is_on_list:
                current_user.friends_routes.append(self.route)
                current_user.save_stats()

            self.close()

        else:
            self.al = User_Doesnt_Exist()

    def cancel(self):
        self.close()

    def get_user(self, name):
        file = str(name) + ".txt"
        with open(file, encoding="utf8") as f:
            table = f.readline().split("\t")
            return User(table[0], table[1], table[2], table[3])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    sys.exit(app.exec_())


