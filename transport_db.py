# Скрипт копирования базы данных s11 с сервера по sftp
import socket
import pysftp
import logging
import warnings
import json
from datetime import date, timedelta, datetime

from PyQt5.QtCore import Qt

from maket.Transpotr_maket import *
from Date_dum import date_dump

warnings.filterwarnings('ignore', '.*Failed to load HostKeys.*')

current_date = date.today()

user_db = 'root'
secret_db = 'PaSdbR00t'
port = 22
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
logging.basicConfig(filename='Transport.log', level=logging.INFO, filemode='a+')

data_json = {}
Time_limit = 100


def chtenie_json(filename):
    try:
        with open(filename) as f:
            return f.read()
    except: print('конфиг не найден')

def zapis_json(filename, host, remoteP, localP):
    with open(filename, 'w') as f:
        data_json = {'host': host, 'remoteP': remoteP, 'localP': localP}
        json.dump(data_json, f)




class Path_file:
    def __init__(self, path, db, data):
        self.db = str(db)
        self.data = data
        self.path = str(path)

    def __str__(self):
        print(f'{self.path}{self.db}.{self.data}.sql.gz')
        return f'{self.path}{self.db}.{self.data}.sql.gz'
        # if self.path == 'remote':
        #     return f'/home/backup/{self.db}.{self.data}.sql.gz'
        # else:
        #     # slesh = r'\\'
        #     return f"C:\SHARE\{'b'}ackup\{self.db}.{self.data}.sql.gz"
        # \\192.168.0.69\arhiv


class Export_DB:
    def __init__(self, host, user, secret, cnopts, remotepath, localpath):
        self.host = host
        self.user = user
        self.secret = secret
        self.cnopts = cnopts
        self.remotepath = remotepath
        self.localpath = localpath

    def scan_dump(self):
        try:
            print(self.remotepath)
            print(self.localpath)
            print(self.host)
            with pysftp.Connection(host=self.host, port=22, username=self.user, password=self.secret, cnopts=self.cnopts) as sftp:
                try:
                    date_dump = []
                    print(self.remotepath)
                    print(f'Соединение установлено в {datetime.now()} ')
                    sftp.cwd(self.remotepath)
                    dir_struct = sftp.listdir_attr()
                    for attr in dir_struct:
                        if attr.filename.split('.')[0] == 's11':
                            # if attr.filename.split('.')[1] == f'{current_date}':
                            x = attr.filename.split('.')[1]
                            date_dump.append(x)
                            # otrisovka = NewCalendar(x)
                            # otrisovka.paintCell()
                        if attr.filename.split('.')[0] == 'mes':
                            # if attr.filename.split('.')[1] == f'{current_date}':
                            # print('Бэкап mes на текущую дату найден')
                            pass
                except:
                    print("ошибка передачи")
                    logging.info("ошибка хоста")
        except:
            print("ошибка хоста")
            logging.info('Ошибка')
            logging.error('Ошибка передачи данных')
        return date_dump




    def transport(self):
        # self.progres_start()
        print('Подключение к серверу...') #12,5%
        ui.progressBar.setValue(12)
        try:
            with pysftp.Connection(host=self.host, port=22, username=self.user, password=self.secret,
                                   cnopts=self.cnopts, ) as sftp:
                print('Подключение к серверу прошло успешно...') #25%
                ui.progressBar.setValue(25)
                ui.progressBar.setFormat('Подключение к серверу прошло успешно...')
                ui.progressBar.setAlignment(Qt.AlignCenter)
                print('Начинаю процесс копирования s11...') #37,5%
                ui.progressBar.setValue(37)
                ui.progressBar.setFormat('Начинаю процесс копирования s11...')
                ui.progressBar.setAlignment(Qt.AlignCenter)
                sftp.get(
                    Path_file(self.remotepath, 's11', f'{ui.calendarWidget.selectedDate().toString("yyyy-MM-dd")}').__str__(),
                    Path_file(self.localpath, 's11', f'{ui.calendarWidget.selectedDate().toString("yyyy-MM-dd")}').__str__()
                )
                print('Процесс копирования дампа s11 завершен') #50%
                ui.progressBar.setValue(50)
                ui.progressBar.setFormat('Процесс копирования дампа s11 завершен')
                ui.progressBar.setAlignment(Qt.AlignCenter)
            with pysftp.Connection(host=self.host, port=22, username=self.user, password=self.secret,
                                   cnopts=self.cnopts, ) as sftp:
                print('Подключение к серверу прошло успешно...') #62,5%
                ui.progressBar.setValue(62)
                ui.progressBar.setFormat('Подключение к серверу прошло успешно...')
                ui.progressBar.setAlignment(Qt.AlignCenter)
                print('Начинаю процесс копирования mes...') #75%
                ui.progressBar.setValue(75)
                ui.progressBar.setFormat('Начинаю процесс копирования mes...')
                ui.progressBar.setAlignment(Qt.AlignCenter)
                sftp.get(
                    Path_file(self.remotepath, 'mes', f'{ui.calendarWidget.selectedDate().toString("yyyy-MM-dd")}').__str__(),
                    Path_file(self.localpath, 'mes', f'{ui.calendarWidget.selectedDate().toString("yyyy-MM-dd")}').__str__()
                )
                print('Процесс копирования дампа mes завершен') #87,5%
                ui.progressBar.setValue(87)
                ui.progressBar.setFormat('Процесс копирования дампа mes завершен')
                ui.progressBar.setAlignment(Qt.AlignCenter)
        except: print('Дамп БД не найден!')
        print('процедура загрузки дампов завершена') #100%
        ui.progressBar.setValue(100)
        ui.progressBar.setFormat('Процедура загрузки дампов завершена')
        ui.progressBar.setAlignment(Qt.AlignCenter)


class Calendar_dump_v2(QtWidgets.QCalendarWidget):
    # global date_dump
    def __init__(self, parent=None):
        QtWidgets.QCalendarWidget.__init__(self, parent)

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        # if date == date.currentDate():
        # print('тут')
        for dat in date_dump:
            # qqdate = QtCore.QDate.fromString(dat, "yyyy-MM-dd")
            # ui.calendarWidget.setSelectedDate(qqdate)
            if date.toString('yyyy-MM-dd') == dat:
                 painter.setBrush(QtGui.QColor(0, 200, 200, 50))
        #         # painter.setPen(QtGui.QPen(QtGui.QColor(0, 200, 200),  3, Qt.SolidLine, Qt.RoundCap))
        #         # painter.setPen(QtGui.QColor(0, 0, 0, 0))
        #         # painter.drawLine(rect.topRight(), rect.topLeft())
        #         # painter.drawLine(rect.topRight(), rect.bottomRight())
        #         # painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        #         # painter.drawLine(rect.topLeft(), rect.bottomLeft())
                 painter.drawRect(rect)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    data_json = chtenie_json('connect.json')
    obj = json.loads(data_json)
    ui.lineEdit.setText(obj['host'])
    ui.lineEdit_2.setText(obj['remoteP'])
    ui.lineEdit_3.setText(obj['localP'])

    def on_click_scan():
        remotepath = ui.lineEdit_2.text()
        localpath = ui.lineEdit_3.text()
        host_db = ui.lineEdit.text()
        expo = Export_DB(host_db, user_db, secret_db, cnopts, remotepath, localpath)
        expo.scan_dump()
        print(expo.scan_dump())
        x = expo.scan_dump()
        with open('Date_dum.py', 'w') as f:
            f.write(f'date_dump = {str(x)}')
        zapis_json('connect.json', host_db, remotepath, localpath)

    def on_click_transport():
        expo = Export_DB(ui.lineEdit.text(), user_db, secret_db, cnopts, ui.lineEdit_2.text(), ui.lineEdit_3.text())
        expo.transport()

    ui.pushButton.clicked.connect(on_click_scan)
    ui.pushButton_2.clicked.connect(on_click_transport)

    sys.exit(app.exec_())




















