import sys
import time
import socket
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRect


class QWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.lcdTimer = QtWidgets.QLCDNumber(5, self)
        self.groupBox1 = QtWidgets.QGroupBox('Proxies', self)
        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.connectButton = QtWidgets.QPushButton("Connect", self)
        self.groupBox2 = QtWidgets.QGroupBox('Proxy session time', self)
        self.fsButton = QtWidgets.QRadioButton('fs.fabiobruno.ru', self)
        self.fs1Button = QtWidgets.QRadioButton('fs1.fabiobruno.ru', self)
        self.proxyLabel = QtWidgets.QLabel('Choose proxy for connect:', self)
        self.cancelButton.clicked.connect(QtWidgets.qApp.quit)

    def set_geometry(self):
        self.lcdTimer.setGeometry(QRect(200, 82, 81, 31))
        self.fsButton.setGeometry(QRect(30, 70, 131, 17))
        self.groupBox1.setGeometry(QRect(20, 50, 131, 92))
        self.fs1Button.setGeometry(QRect(30, 110, 131, 17))
        self.groupBox2.setGeometry(QRect(180, 50, 121, 92))
        self.proxyLabel.setGeometry(QRect(21, 16, 281, 21))
        self.cancelButton.setGeometry(QRect(227, 159, 75, 23))
        self.connectButton.setGeometry(QRect(137, 159, 75, 23))

    def lbutton_group(self):
        rbox = QtWidgets.QButtonGroup()
        rbox.addButton(self.fsButton)
        rbox.addButton(self.fs1Button)
        rbox.setParent(self)

    def show_elements(self):
        for element in [self.fsButton, self.fs1Button, self.groupBox1,
                        self.groupBox2, self.lcdTimer, self.proxyLabel,
                        self.cancelButton, self.connectButton]:
            element.show()

    def create_ui(self):
        self.setWindowTitle('Viaborsa')
        self.setWindowIcon(QtGui.QIcon('desktop.ico'))
        self.setFixedSize(320, 200)
        self.set_geometry()
        self.groupBox1.setEnabled(False)
        self.groupBox2.setEnabled(False)
        self.lbutton_group()
        self.fsButton.setChecked(True)
        # noinspection PyTypeChecker
        self.lcdTimer.setSegmentStyle(2)
        self.lcdTimer.segmentStyle()
        self.show_elements()


class Knocker(object):
    def __init__(self, addr, ports: list):
        self.ports = ports
        self.addr = addr
        self.delay = 0.5

    def knock(self):
        last_index = len(self.ports) - 1
        for i, port in enumerate(self.ports):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setblocking(False)
            socket_address = (self.addr, int(port))
            s.sendto(b'', socket_address)
            print('Sent to', self.addr, port)
            s.close()
            if self.delay and i != last_index:
                time.sleep(self.delay)


class Connector:
    def __init__(self, qw):
        self.qwindow = qw

    def __call__(self, *args, **kwargs):
        proxy = '1.1.1.1' if self.qwindow.fsButton.isChecked() else '2.2.2.2'
        ports = [1, 2, 3, 4]
        knock = Knocker(proxy, ports)
        knock.knock()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('desktop.ico'))
    qw = QWindow()
    qw.connectButton.clicked.connect(Connector(qw))
    qw.create_ui()
    qw.show()
    sys.exit(app.exec_())
