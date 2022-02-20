#!/usr/bin/env python3
"""POTAto helps chasers hunt POTA activators. Find out more about POTA at https://pota.app"""
import xmlrpc.client
import sys
import os
import logging
from datetime import datetime, timezone
from json import loads
import re
import psutil
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QFontDatabase, QBrush, QColor
import requests

logging.basicConfig(level=logging.WARNING)


def relpath(filename):
    """
    Checks to see if program has been packaged with pyinstaller.
    If so base dir is in a temp folder.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = getattr(sys, "_MEIPASS")
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


def load_fonts_from_dir(directory):
    """loads in font families"""
    font_families = set()
    for file_index in QDir(directory).entryInfoList(["*.ttf", "*.woff", "*.woff2"]):
        _id = QFontDatabase.addApplicationFont(file_index.absoluteFilePath())
        font_families |= set(QFontDatabase.applicationFontFamilies(_id))
    return font_families


class MainWindow(QtWidgets.QMainWindow):
    """The main window class"""

    potaurl = "https://api.pota.app/spot/activator"
    bw = {}
    lastclicked = ""
    workedlist = []
    spots = None

    def __init__(self, parent=None):
        """Initialize class variables"""
        isflrunning = self.checkflrun()
        super().__init__(parent)
        uic.loadUi(self.relpath("dialog.ui"), self)
        if isflrunning is True:
            print("flrig is running")
            self.listWidget.clicked.connect(self.spotclicked)
        else:
            print("flrig is not running")
        self.listWidget.doubleClicked.connect(self.item_double_clicked)
        self.comboBox_mode.currentTextChanged.connect(self.getspots)
        self.comboBox_band.currentTextChanged.connect(self.getspots)
        self.server = xmlrpc.client.ServerProxy("http://localhost:12345")

    @staticmethod
    def relpath(filename: str) -> str:
        """
        If the program is packaged with pyinstaller,
        this is needed since all files will be in a temp
        folder during execution.
        """
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_path = getattr(sys, "_MEIPASS")
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filename)

    def getspots(self):
        """Gets activator spots from pota.app"""
        self.time.setText(str(datetime.now(timezone.utc)).split()[1].split(".")[0][0:5])
        try:
            request = requests.get(self.potaurl, timeout=15.0)
            request.raise_for_status()
        except requests.ConnectionError as err:
            self.listWidget.addItem(f"Network Error: {err}")
            return
        except requests.exceptions.Timeout as err:
            self.listWidget.addItem(f"Timeout Error: {err}")
            return
        except requests.exceptions.HTTPError as err:
            self.listWidget.addItem(f"HTTP Error: {err}")
            return
        except requests.exceptions.RequestException as err:
            self.listWidget.addItem(f"Error: {err}")
            return
        self.spots = loads(request.text)
        self.showspots()

    def showspots(self):
        """Display spots in a list"""
        self.listWidget.clear()
        for i in self.spots:
            mode_selection = self.comboBox_mode.currentText()
            if mode_selection == "-FT*" and i["mode"][:2] == "FT":
                continue
            if (
                mode_selection == "All"
                or mode_selection == "-FT*"
                or i["mode"] == mode_selection
            ):
                band_selection = self.comboBox_band.currentText()
                if (
                    band_selection == "All"
                    or self.getband(i["frequency"].split(".")[0]) == band_selection
                ):
                    spot = (
                        f"{i['spotTime'].split('T')[1][0:5]} "
                        f"{i['activator'].rjust(10)} "
                        f"{i['reference'].ljust(7)} "
                        f"{i['frequency'].split('.')[0].rjust(6)} "
                        f"{i['mode']}"
                    )
                    self.listWidget.addItem(spot)
                    if spot[5:] == self.lastclicked[5:]:
                        founditem = self.listWidget.findItems(
                            spot[5:],
                            QtCore.Qt.MatchFlag.MatchContains,  # pylint: disable=no-member
                        )
                        founditem[0].setSelected(True)
                    if i["activator"] in self.workedlist:
                        founditem = self.listWidget.findItems(
                            i["activator"],
                            QtCore.Qt.MatchFlag.MatchContains,  # pylint: disable=no-member
                        )
                        founditem[0].setBackground(QBrush(QColor.fromRgb(0, 128, 0)))

    def spotclicked(self):
        """
        If flrig is running on this PC, tell it to tune to the spot freq and change mode.
        Otherwise die gracefully.
        """

        try:
            item = self.listWidget.currentItem()
            line = item.text().split()
            self.lastclicked = item.text()
            freq = line[3]
            mode = line[4].upper()
            combfreq = freq + "000"
            self.server.rig.set_frequency(float(combfreq))
            if mode == "SSB":
                if int(combfreq) > 10000000:
                    mode = "USB"
                else:
                    mode = "LSB"
            self.server.rig.set_mode(mode)
        except:
            pass

    def item_double_clicked(self):
        """If a list item is double clicked a green highlight will be toggles"""
        item = self.listWidget.currentItem()
        line = item.text().split()
        if line[1] in self.workedlist:
            self.workedlist.remove(line[1])
        else:
            self.workedlist.append(line[1])
        self.showspots()

    @staticmethod
    def getband(freq):
        """converts a frequency into a ham band"""
        if freq.isnumeric():
            frequency = int(float(freq)) * 1000
            if 2000000 > frequency > 1800000:
                return "160"
            if 4000000 > frequency > 3500000:
                return "80"
            if 5406000 > frequency > 5330000:
                return "60"
            if 7300000 > frequency > 7000000:
                return "40"
            if 10150000 > frequency > 10100000:
                return "30"
            if 14350000 > frequency > 14000000:
                return "20"
            if 18168000 > frequency > 18068000:
                return "17"
            if 21450000 > frequency > 21000000:
                return "15"
            if 24990000 > frequency > 24890000:
                return "12"
            if 29700000 > frequency > 28000000:
                return "10"
            if 54000000 > frequency > 50000000:
                return "6"
            if 148000000 > frequency > 144000000:
                return "2"
        else:
            return "0"

    @staticmethod
    def checkflrun():
        """checks to see if flrig is in the active process list"""
        reg = "flrig"
        found = False

        for proc in psutil.process_iter():
            if found is False:
                if bool(re.match(reg, proc.name().lower())):
                    found = True
        return found


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    font_dir = relpath("font")
    families = load_fonts_from_dir(os.fspath(font_dir))
    logging.info(families)
    window = MainWindow()
    window.show()
    window.getspots()
    timer = QtCore.QTimer()
    timer.timeout.connect(window.getspots)
    timer.start(30000)
    app.exec()
