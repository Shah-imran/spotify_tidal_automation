from gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
import sys
import os
import var
from time import sleep
from threading import Thread
import json
import db
import stream


global app
class MyGui(Ui_MainWindow, QtWidgets.QWidget):
    def __init__(self, mainWindow):
        Ui_MainWindow.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(mainWindow)


class myMainClass():
    def __init__(self):

        Thread(target=refresh_main_acc_table, daemon=True).start()

        GUI.lineEdit_db_ip.setText(str(var.db_ip))
        GUI.lineEdit_db_port.setText(str(var.db_port))
        GUI.lineEdit_db_user.setText(str(var.db_user))
        GUI.lineEdit_db_pass.setText(str(var.db_pass))
        GUI.lineEdit_proxy_user.setText(str(var.proxy_user))
        GUI.lineEdit_proxy_pass.setText(str(var.proxy_pass))
        GUI.lineEdit_time_duration.setText(str(var.time_duration))
        GUI.lineEdit_proxy_port.setText(str(var.proxy_port))

        GUI.pushButton_create_db_table.clicked.connect(self.create_db_table)
        GUI.pushButton_create_demo_playlist.clicked.connect(self.create_demo_playlist)
        GUI.pushButton_account_refresh_table.clicked.connect(self.refresh_account_table)
        GUI.pushButton_account_add_db.clicked.connect(self.add_account)
        GUI.pushButton_accRemFromDb.clicked.connect(self.remove_account)
        GUI.pushButton_songsAddToDb.clicked.connect(self.add_song)
        GUI.pushButton_songsRemFromDb.clicked.connect(self.remove_song)
        GUI.pushButton_viewShowPlaylist.clicked.connect(self.get_playlist)
        GUI.pushButton_songsRefreshTable.clicked.connect(self.refresh_song_table)
        GUI.pushButton_updateMainTable.clicked.connect(self.update_playlist)
        GUI.pushButton_mainStart.clicked.connect(self.start)
        GUI.pushButton_mainStartAll.clicked.connect(self.start)
        GUI.pushButton_mainStop.clicked.connect(self.stop)
        GUI.pushButton_stop_all.clicked.connect(self.stop_all)

    def start(self):
        var.stop_list = list()
        GUI.pushButton_mainStartAll.setDisabled(True)
        GUI.pushButton_mainStart.setDisabled(True)
        update_var()
        var.stop = False
        var.stop_all = False
        Thread(target=start_streaming, daemon=True).start()

    def stop(self):
        GUI.pushButton_mainStartAll.setDisabled(False)
        GUI.pushButton_mainStart.setDisabled(False)
        var.stop_all = False
        var.stop = True
        Thread(target=stoping, daemon=True).start()

    def stop_all(self):
        GUI.pushButton_mainStartAll.setDisabled(False)
        GUI.pushButton_mainStart.setDisabled(False)
        var.stop = False
        var.stop_all = True
        Thread(target=stoping_all, daemon=True).start()

    def update_playlist(self):
        update_var()
        Thread(target=update_playlist, daemon=True).start()
        
    def get_playlist(self):
        update_var()
        playlist = GUI.lineEdit_viewPlaylist.text().strip()
        Thread(target=get_playlist, daemon=True, args=[playlist,]).start()
        
    def refresh_song_table(self):
        update_var()
        Thread(target=get_songs, daemon=True).start()

    def remove_account(self):
        update_var()
        id = GUI.lineEdit_accId.text().strip()
        Thread(target=remove_account, daemon=True, args=[id,]).start()

    def remove_song(self):
        update_var()
        id = GUI.lineEdit_songsId.text().strip()
        Thread(target=remove_song, daemon=True, args=[id,]).start()

    def add_song(self):
        update_var()
        stream = GUI.lineEdit_songsLink.text().strip()
        name = GUI.lineEdit_songsName.text().strip()
        playlist = GUI.lineEdit_songsPlaylist.text().strip()
        self.check_radio()
        args = (stream, name, playlist, var.site)
        Thread(target=add_song,daemon=True, args=args).start()

    def add_account(self):
        update_var()
        username = GUI.lineEdit_accUsername.text().strip()
        password = GUI.lineEdit_accPass.text().strip()
        playlist = GUI.lineEdit_accPlaylist.text().strip()
        proxy_ip = GUI.lineEdit_proxy_ip.text().strip()
        self.check_radio()
        args = (username, password, playlist, proxy_ip, var.site)
        Thread(target=add_account,daemon=True, args=args).start()

    def refresh_account_table(self):
        update_var()
        Thread(target=populate_account_table, daemon=True, args=[GUI.tableWidget_accTable,]).start()

    def create_demo_playlist(self):
        update_var()
        Thread(target=create_demo_playlist, daemon=True).start()

    def create_db_table(self):
        update_var()
        Thread(target=db.create_db, daemon=True).start()

    def check_radio(self):
        var.site = "spotify"
        if GUI.radioButton_tidal.isChecked():
            var.site = "tidal"

def stoping():
    for item in GUI.tableWidget_mainTable.selectionModel().selectedRows():
        id = int(GUI.tableWidget_mainTable.item(item.row(), 0).text())
        var.stop_list.append(id)
        GUI.tableWidget_mainTable.setItem(item.row(),6, QTableWidgetItem("Stopped"))

def stoping_all():
    for count in range(var.main_table_row_count):
        if GUI.tableWidget_mainTable.item(count, 6).text() == "Running":
            GUI.tableWidget_mainTable.setItem(count, 6, QTableWidgetItem("Stopped"))

def start_streaming():
    for item in GUI.tableWidget_mainTable.selectionModel().selectedRows():
        id = int(GUI.tableWidget_mainTable.item(item.row(), 0).text())
        username = GUI.tableWidget_mainTable.item(item.row(), 1).text()
        password = GUI.tableWidget_mainTable.item(item.row(), 2).text()
        playlist = GUI.tableWidget_mainTable.item(item.row(), 3).text()
        proxy_ip = GUI.tableWidget_mainTable.item(item.row(), 4).text()
        site = GUI.tableWidget_mainTable.item(item.row(), 5).text()
        GUI.tableWidget_mainTable.setItem(item.row(),6, QTableWidgetItem("Running"))
        args = (id, username, password, playlist, proxy_ip, site)
        Thread(target=stream.main, daemon=True, args=args).start()
        sleep(10)


def update_var():
    try:
        var.db_ip = GUI.lineEdit_db_ip.text().strip()
        var.db_port = int(GUI.lineEdit_db_port.text().strip())
        var.db_user = GUI.lineEdit_db_user.text().strip()
        var.db_pass = GUI.lineEdit_db_pass.text().strip()
        var.proxy_user = GUI.lineEdit_proxy_user.text().strip()
        var.proxy_pass = GUI.lineEdit_proxy_pass.text().strip()
        var.proxy_port = int(GUI.lineEdit_proxy_port.text().strip())
        var.time_duration = int(GUI.lineEdit_time_duration.text().strip())
        data = {"config": 
                {
                    "ip": var.db_ip, 
                    "port": var.db_port, 
                    "db_user": var.db_user, 
                    "db_pass": var.db_pass,
                    "db_name": "stream", 
                    "proxy_user": var.proxy_user,
                    "proxy_pass": var.proxy_pass,
                    "proxy_port": var.proxy_port,
                    "time_duration": var.time_duration
                }
                }
            # data = json.loads(data)
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file)
    except Exception as e:
        print("Exeception occured at update_var :{}".format(e))


def update_playlist():
    for item in GUI.tableWidget_mainTable.selectionModel().selectedRows():
        print(item.row())
        id = int(GUI.tableWidget_mainTable.item(item.row(), 0).text())
        playlist = GUI.tableWidget_mainTable.item(item.row(), 3).text()
        proxy_ip = GUI.tableWidget_mainTable.item(item.row(), 4).text()
        break
    
    try:
        conn = db.db_ceate()
        conn.update_user_playlist( id, playlist, proxy_ip)
        conn.close()
    except:
        pass
    populate_account_table(GUI.tableWidget_mainTable)

def refresh_main_acc_table():
    populate_account_table(GUI.tableWidget_mainTable)

def add_song( stream, name, playlist, site):
    conn = db.db_ceate()
    conn.add_song((stream, name, playlist, site))
    conn.close()
    get_songs()

def remove_song(id):
    id = int(id)
    print(id)
    conn = db.db_ceate()
    conn.remove_song(id)
    conn.close()
    get_songs()

def get_playlist(playlist):
    conn = db.db_ceate()
    result = conn.get_playlist(playlist)
    conn.close()
    print(len(result))
    print(result)
    
    populate_song_table(result, GUI.tableWidget_viewPlayListTable)

def get_songs():
    conn = db.db_ceate()
    result = conn.fetch_table("songs")
    conn.close()
    print(len(result))
    populate_song_table(result, GUI.tableWidget_songsTable)

def populate_song_table(result, item):
    item.setRowCount(len(result))
    for row in range(len(result)):
        for col in range(6):
            item.setItem(row,col, QTableWidgetItem(str(result[row][col])))

def create_demo_playlist():
    con = db.db_ceate()
    con.create_demo_playlist()
    con.close()

def populate_account_table(item):
    conn = db.db_ceate()
    result = conn.fetch_table("users")
    conn.close()
    var.main_table_row_count = len(result)
    print(var.main_table_row_count)
    item.setRowCount(var.main_table_row_count)
    for row in range(var.main_table_row_count):
        for col in range(6):
            item.setItem(row,col, QTableWidgetItem(str(result[row][col])))

def add_account(username, password, playlist, proxy_ip, site):
    print(username, password, playlist, proxy_ip, site)
    conn = db.db_ceate()
    conn.add_account((username, password, playlist, proxy_ip, site))
    conn.close()
    populate_account_table(GUI.tableWidget_accTable)

def remove_account(id):
    id = int(id)
    print(id)
    conn = db.db_ceate()
    conn.remove_account(id)
    conn.close()
    populate_account_table(GUI.tableWidget_accTable)

if __name__ == '__main__':

    global app
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    try:
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        p = resource_path('dodo.ico')
        mainWindow.setWindowIcon(QtGui.QIcon(p))
    except Exception as e:
        print(e)

    mainWindow.setWindowFlags(mainWindow.windowFlags() |
                          QtCore.Qt.WindowMinimizeButtonHint |
                          QtCore.Qt.WindowSystemMenuHint)

    GUI = MyGui(mainWindow)
    mainWindow.show()

    myMC = myMainClass()

    app.exec_()
    update_var()
    print("Exit")
    sys.exit()