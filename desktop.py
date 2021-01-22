import sys
import time
import socket
from PyQt5 import QtCore, QtWidgets, QtGui

PROXY = ['178.62.249.204', '161.35.198.236']
PORTS = [33247, 18071, 59601, 27522]


class QWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.lcdTimer = QtWidgets.QLCDNumber(5, self)
        self.textLine = QtWidgets.QLineEdit(parent=self)
        self.groupBox1 = QtWidgets.QGroupBox('Proxies', self)
        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.connectButton = QtWidgets.QPushButton("Connect", self)
        self.groupBox2 = QtWidgets.QGroupBox('Proxy session time', self)
        self.fsButton = QtWidgets.QRadioButton('fs.fabiobruno.ru', self)
        self.fs1Button = QtWidgets.QRadioButton('fs1.fabiobruno.ru', self)
        self.proxyLabel = QtWidgets.QLabel('Choose proxy for connect:', self)
        self.cancelButton.clicked.connect(QtWidgets.qApp.quit)
        self.connectButton.clicked.connect(Connector(self))
        self.textLine.setReadOnly(True)

    def set_geometry(self):
        self.lcdTimer.setGeometry(QtCore.QRect(200, 82, 81, 31))
        self.fsButton.setGeometry(QtCore.QRect(30, 70, 131, 17))
        self.textLine.setGeometry(QtCore.QRect(22, 161, 101, 20))
        self.groupBox1.setGeometry(QtCore.QRect(20, 50, 131, 92))
        self.fs1Button.setGeometry(QtCore.QRect(30, 110, 131, 17))
        self.groupBox2.setGeometry(QtCore.QRect(180, 50, 121, 92))
        self.proxyLabel.setGeometry(QtCore.QRect(21, 16, 281, 21))
        self.cancelButton.setGeometry(QtCore.QRect(227, 159, 75, 23))
        self.connectButton.setGeometry(QtCore.QRect(137, 159, 75, 23))

    def lbutton_group(self):
        rbox = QtWidgets.QButtonGroup()
        rbox.addButton(self.fsButton)
        rbox.addButton(self.fs1Button)
        rbox.setParent(self)

    def show_elements(self):
        for element in [self.fsButton, self.fs1Button, self.groupBox1,
                        self.groupBox2, self.lcdTimer, self.proxyLabel,
                        self.cancelButton, self.connectButton, self.textLine]:
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
    def __init__(self, addr, ports: list, delay):
        self.ports = ports
        self.addr = addr
        self.delay = delay

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


class Timer(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(11):
            self.sleep(1)
            self.signal.emit(10-i)


class Connector:
    def __init__(self, qwindow):
        self.qwindow = qwindow
        self.thread = None

    def __call__(self, *args, **kwargs):
        proxy = PROXY[0] if self.qwindow.fsButton.isChecked() else PROXY[1]
        ports = PORTS
        knock = Knocker(proxy, ports, delay=0.5)
        knock.knock()
        if not self.thread:
            self.thread = Timer()
            qw.lcdTimer.display(10)
            qw.connectButton.setDisabled(True)
            self.thread.signal.connect(self.on_change)
            self.thread.finished.connect(self.on_finished)
            self.thread.start()

    def on_finished(self):
        qw.connectButton.setDisabled(False)
        self.thread.signal.disconnect(self.on_change)
        self.thread.finished.disconnect(self.on_finished)
        self.thread = None

    @staticmethod
    def on_change(time):
        qw.lcdTimer.value = time
        qw.lcdTimer.display(time)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('desktop.ico'))
    qw = QWindow()
    qw.create_ui()
    qw.show()
    sys.exit(app.exec_())
