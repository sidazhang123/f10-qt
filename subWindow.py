
from PyQt5.QtCore import Qt,pyqtSlot,pyqtSignal
from PyQt5.QtGui import QIcon,QCloseEvent
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from common.loadPage import loadReprPage


class SubWindow(QWidget):
    rmWinSig=pyqtSignal(str,int,int)
    def __init__(self, title, data,rmFn,h,w):
        super(SubWindow, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.rmWinSig.connect(rmFn)
        self.chrome_widget = ChromeWidget(self, data,title)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.chrome_widget)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)
        self.resize(w,h)
        self.setWindowOpacity(0.9)
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.title=title
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('pages/icon.ico'))

    @pyqtSlot(bool)
    def toggle_stay_on_top(self, b):
        if b:
            self.setWindowFlags(
                Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
        self.show()



    @pyqtSlot(int)
    def closeEvent(self, event):
        self.rmWinSig.emit(self.title,self.size().height(),self.size().width())
        self.close()


class ChromeWidget(QWidget):
    def __init__(self, parent, data, win):
        super(ChromeWidget, self).__init__(parent)
        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self.browser.page().setWebChannel(self.channel)
        self.browser.setHtml(loadReprPage(data, win))
        self.__layout()
        # self.setFixedSize(690, 600)

    def __layout(self):
        self.vBox = QVBoxLayout()
        self.hBox = QVBoxLayout()
        self.hBox.addWidget(self.browser)
        self.vBox.addLayout(self.hBox)
        self.setLayout(self.vBox)
        self.hBox.setContentsMargins(0, 0, 0, 0)

        self.vBox.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
