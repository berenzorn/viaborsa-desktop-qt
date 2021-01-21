import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRect


class QWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.lcdTimer = QtWidgets.QLCDNumber()
        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.connectButton = QtWidgets.QPushButton("Connect", self)
        self.fsButton = QtWidgets.QRadioButton('fs.fabiobruno.ru')
        self.fs1Button = QtWidgets.QRadioButton('fs1.fabiobruno.ru')
        self.proxyLabel = QtWidgets.QLabel('Choose proxy for connect:')
        self.groupBox1 = QtWidgets.QGroupBox('Proxies', self)
        self.groupBox2 = QtWidgets.QGroupBox('Proxy session time', self)
        self.cancelButton.clicked.connect(QtWidgets.qApp.quit)

    def group_box(self):
        self.groupBox1.setGeometry(QRect(20, 50, 131, 92))
        self.groupBox2.setGeometry(QRect(180, 50, 121, 92))
        self.groupBox1.setEnabled(False)
        self.groupBox2.setEnabled(False)
        self.groupBox1.show()
        self.groupBox2.show()

    def create_ui(self):
        self.setWindowTitle('Viaborsa')
        self.setWindowIcon(QtGui.QIcon('desktop.ico'))
        self.setFixedSize(320, 200)
        self.connectButton.setGeometry(137, 159, 75, 23)
        self.cancelButton.setGeometry(227, 159, 75, 23)
        self.connectButton.show()
        self.cancelButton.show()
        self.group_box()
        self.fsButton.setChecked(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('desktop.ico'))
    qw = QWindow()
    qw.create_ui()
    qw.show()
    sys.exit(app.exec_())
