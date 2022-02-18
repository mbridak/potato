#!/usr/bin/env python3

import logging

logging.basicConfig(level=logging.WARNING)

import xmlrpc.client
import requests, sys, os
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QFontDatabase
from datetime import datetime, timezone
from json import loads


def relpath(filename):
    try:
        base_path = sys._MEIPASS  # pylint: disable=no-member
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


def load_fonts_from_dir(directory):
    families = set()
    for fi in QDir(directory).entryInfoList(["*.ttf", "*.woff", "*.woff2"]):
        _id = QFontDatabase.addApplicationFont(fi.absoluteFilePath())
        families |= set(QFontDatabase.applicationFontFamilies(_id))
    return families


class MainWindow(QtWidgets.QMainWindow):
    potaurl = "https://api.pota.app/spot/activator"
    rigctld_addr = "127.0.0.1"
    rigctld_port = 4532
    bw = {}
    lastclicked = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(self.relpath("dialog.ui"), self)
        #self.listWidget.clicked.connect(self.spotclicked)
        self.comboBox_mode.currentTextChanged.connect(self.getspots)
        self.comboBox_band.currentTextChanged.connect(self.getspots)
        self.server = xmlrpc.client.ServerProxy("http://localhost:12345")

    def relpath(self, filename):
        try:
            base_path = sys._MEIPASS  # pylint: disable=no-member
        except:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filename)

    def getspots(self):
        self.time.setText(str(datetime.now(timezone.utc)).split()[1].split(".")[0][0:5])
        try:
            request = requests.get(self.potaurl, timeout=15.0)
            request.raise_for_status()
        except requests.ConnectionError as e:
            self.listWidget.addItem(f"Network Error: {e}")
            return
        except requests.exceptions.Timeout as e:
            self.listWidget.addItem("Timeout Error: {e}")
            return
        except requests.exceptions.HTTPError as e:
            self.listWidget.addItem("HTTP Error: {e}")
            return
        except requests.exceptions.RequestException as e:
            self.listWidget.addItem("Error: {e}")
            return
        spots = loads(request.text)
        self.listWidget.clear()
        justonce = []
        for i in spots:
            modeSelection = self.comboBox_mode.currentText()
            if modeSelection == "-FT*" and i["mode"][:2] == "FT":
                continue
            if (
                modeSelection == "All"
                or modeSelection == "-FT*"
                or i["mode"] == modeSelection
            ):
                bandSelection = self.comboBox_band.currentText()
                if (
                    bandSelection == "All"
                    or self.getband(i["frequency"].split(".")[0]) == bandSelection
                ):
                    spot = f"{i['spotTime'].split('T')[1][0:5]} {i['activator'].rjust(10)} {i['reference'].ljust(7)} {i['frequency'].split('.')[0].rjust(5)} {i['mode']}"
                    self.listWidget.addItem(spot)
                    if spot[5:] == self.lastclicked[5:]:
                        founditem = self.listWidget.findItems(
                            spot[5:], QtCore.Qt.MatchFlag.MatchContains
                        )
                        founditem[0].setSelected(True)

    # def spotclicked(self):
    #     """
    #     If flrig is running on this PC, tell it to tune to the spot freq and change mode.
    #     Otherwise die gracefully.
    #     """

    #     try:
    #         item = self.listWidget.currentItem()
    #         line = item.text().split()
    #         self.lastclicked = item.text()
    #         freq = line[3]
    #         mode = line[4].upper()
    #         combfreq = freq + "000"
    #         self.server.rig.set_frequency(float(combfreq))
    #         if mode == "SSB":
    #             if int(combfreq) > 10000000:
    #                 mode = "USB"
    #             else:
    #                 mode = "LSB"
    #         self.server.rig.set_mode(mode)
    #     except:
    #         pass

    def getband(self, freq):
        if freq.isnumeric():
            frequency = int(float(freq)) * 1000
            if frequency > 1800000 and frequency < 2000000:
                return "160"
            if frequency > 3500000 and frequency < 4000000:
                return "80"
            if frequency > 5330000 and frequency < 5406000:
                return "60"
            if frequency > 7000000 and frequency < 7300000:
                return "40"
            if frequency > 10100000 and frequency < 10150000:
                return "30"
            if frequency > 14000000 and frequency < 14350000:
                return "20"
            if frequency > 18068000 and frequency < 18168000:
                return "17"
            if frequency > 21000000 and frequency < 21450000:
                return "15"
            if frequency > 24890000 and frequency < 24990000:
                return "12"
            if frequency > 28000000 and frequency < 29700000:
                return "10"
            if frequency > 50000000 and frequency < 54000000:
                return "6"
            if frequency > 144000000 and frequency < 148000000:
                return "2"
        else:
            return "0"


def main():
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


if __name__ == "__main__":
    main()
