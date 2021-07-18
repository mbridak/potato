#!/usr/bin/env python3
import requests, sys, os, socket, json
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from datetime import datetime,timezone

class MainWindow(QtWidgets.QMainWindow):
    potaurl="https://api.pota.us/spot/activator"
    rigctld_addr = "127.0.0.1"
    rigctld_port = 4532
    bw = {}
    lastclicked = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(self.relpath("dialog.ui"), self)
        self.listWidget.clicked.connect(self.spotclicked)
        self.bw['LSB'] = '2400'
        self.bw['USB'] = '2400'
        self.bw['FM'] = '15000'
        self.bw['CW'] = '200'

    def relpath(self, filename):
        try:
            base_path = sys._MEIPASS # pylint: disable=no-member
        except:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filename)

    def getspots(self):
        self.time.setText(str(datetime.now(timezone.utc)).split()[1].split(".")[0][0:5])
        request=requests.get(self.potaurl,timeout=15.0)
        spots = json.loads(request.text)
        self.listWidget.clear()
        justonce=[]

        for i in spots:
            spot=f"{i['spotTime'].split('T')[1][0:5]} {i['activator'].rjust(10)} {i['reference'].ljust(7)} {i['frequency'].split('.')[0].rjust(5)} {i['mode']}"
            """
            i['activatorCallsign']=i['activatorCallsign'].replace("\n", "").upper()
            i['activatorCallsign']=i['activatorCallsign'].replace(" ", "")
            if i['activatorCallsign'] in justonce:
                continue
            justonce.append(i['activatorCallsign'])
            summit = f"{i['associationCode'].rjust(3)}/{i['summitCode'].rjust(6)}" # {i['summitDetails']}
            """
            self.listWidget.addItem(spot)
            if spot[5:] == self.lastclicked[5:]:
                founditem = self.listWidget.findItems(spot[5:], QtCore.Qt.MatchFlag.MatchContains)
                founditem[0].setSelected(True)
            

    def spotclicked(self):
        """
        If rigctld is running on this PC, tell it to tune to the spot freq.
        Otherwise die gracefully.
        """

        try:
            item = self.listWidget.currentItem()
            line = item.text().split()
            self.lastclicked = item.text()
            freq = line[3]
            mode = line[4].upper()
            combfreq = freq+"000"
            radiosocket = socket.socket()
            radiosocket.settimeout(0.1)
            radiosocket.connect((self.rigctld_addr, self.rigctld_port))
            command = 'F'+combfreq+'\n'
            radiosocket.send(command.encode('ascii'))
            if mode == 'SSB':
                if int(combfreq) > 10000000:
                    mode = 'USB'
                else:
                    mode = 'LSB'
            command = 'M '+mode+ ' ' + self.bw[mode] + '\n'
            radiosocket.send(command.encode('ascii'))
            radiosocket.shutdown(socket.SHUT_RDWR)
            radiosocket.close()
        except:
            pass 

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.show()
window.getspots()
timer = QtCore.QTimer()
timer.timeout.connect(window.getspots)
timer.start(30000)
app.exec()