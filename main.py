import json
import sys
import threading
import time
from datetime import datetime

import psutil
import win32gui
from PyQt5.QtCore import pyqtSlot, QObject, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from pynput import keyboard

import subWindow
from apply_strat import apply_strat
from common import loadPage, fetch
from common.genTemp.genF10Template import genF10Temp
from common.genTemp.genF10aTemplate import genF10aTemp
from common.genTemp.genF10bTemplate import genF10bTemp
from common.genTemp.genF11Template import genF11Temp
from common.genTemp.genF12Template import genF12Temp


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.old_name = [""]
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._chrome_widget = ChromeWidget(self, self.old_name)
        self.backend = self._chrome_widget.backend
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self._chrome_widget)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)
        self.setFixedSize(930, 580)
        self.setWindowOpacity(0.9)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('f10-qt')
        self.setWindowIcon(QIcon('pages/icon.ico'))

        # listen the app and notify subwindows on the name
        threading.Thread(target=self.tdxNotifier).start()

        self.rctrl_pressed = False
        threading.Thread(target=self.bindKeyPressListener).start()

        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("f10-qt")

    def tdxNotifier(self):
        for name in self.tdxListener():
            if len(name)>0 and self.backend.loaded:
                for win in self.backend.loaded_data:
                    threading.Thread(target=self.backend.notify_subwin, args=(win, name)).start()

    def tdxListener(self):
        from func_timeout import func_timeout, FunctionTimedOut

        while True:
            hwnd = win32gui.FindWindow('TdxW_MainFrame_Class', None)
            hWndChildList = []
            win32gui.EnumChildWindows(hwnd, lambda hWnd, param: param.append(hWnd), hWndChildList)
            for h in hWndChildList:
                try:
                    title = func_timeout(0.1, win32gui.GetWindowText, args=(h,))
                except FunctionTimedOut:
                    title=""
                if title.startswith('分析图表-'):
                    while True:
                        name = win32gui.GetWindowText(h).replace('分析图表-', '').replace(' ', '')
                        if name != self.old_name[0]:
                            self.old_name[0] = name
                            yield name
                        time.sleep(0.2)
            time.sleep(3)

    def onKeyPress(self, key):

        if key == keyboard.Key.ctrl_r:
            self.rctrl_pressed = True
        elif self.rctrl_pressed and key == keyboard.Key.shift_r:

            self.backend.win_conf["topmost"] = not self.backend.win_conf["topmost"]
            # use slot to emit signal to let the subwindows setting their flags themselves
            self.backend.toggleTopmostSig.emit(self.backend.win_conf["topmost"])

        elif self.backend.win_conf["boss"] and (key == keyboard.Key.alt_l or key == keyboard.KeyCode(char='x')):
            self.closeEvent(1)


    def onKeyRelease(self, key):
        if key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = False

    def bindKeyPressListener(self):
        with keyboard.Listener(on_press=self.onKeyPress, on_release=self.onKeyRelease) as listener:
            listener.join()


    def closeEvent(self, event):
        print("called closing")
        # start a new process to write disk & kill qweb processes
        with open("pref.json", "w", encoding="utf-8-sig") as f:
            json.dump(self.backend.win_conf, f)
        for proc in psutil.process_iter():
            if proc.name() == "QtWebEngineProcess.exe":
                proc.kill()
        # after the above process started, exit the ui
        os._exit(-1)


class Router:
    def __init__(self, browser):
        self.browser = browser
        self.boss=False
        self.table = {"home": self.__loadMain, "f10_conf": self.__loadF10Conf,
                      "f10a_supplement_conf": self.__loadF10aSupplementConf,
                      "f10b_shareholder_conf": self.__loadF10bShareholderConf,
                      "f11_industry_conf": self.__loadF11Industry,
                      "f12_finance_conf": self.__loadF12Finance}

    def nav(self, path):
        self.table[path]()

    def __loadMain(self): self.browser.setHtml(loadPage.loadMain(self.boss))

    def __loadF10Conf(self): self.browser.setHtml(loadPage.loadF10Conf())

    def __loadF10aSupplementConf(self): self.browser.setHtml(loadPage.loadF10aSupplementConf())

    def __loadF10bShareholderConf(self): self.browser.setHtml(loadPage.loadF10bShareholderConf())

    def __loadF11Industry(self): self.browser.setHtml(loadPage.loadF11IndustryConf())

    def __loadF12Finance(self): self.browser.setHtml(loadPage.loadF12Finance())

class Backend(QObject):
    toggleTopmostSig = pyqtSignal(bool)
    closeSig = pyqtSignal(int)

    def __init__(self, router, cur_name):
        super(Backend, self).__init__()
        self.win_conf = json.loads(open("pref.json", "r", encoding="utf-8-sig").read())
        router.boss =self.win_conf["boss"]
        self.router = router
        self.cur_name = cur_name
        self.subWindows = dict()
        self.loaded_data = dict()
        self.loaded = False

        self.genTemp = {"f10": genF10Temp, "f10a_supplement": genF10aTemp, "f10b_shareholder": genF10bTemp,
                        "f11_industry": genF11Temp, "f12_finance": genF12Temp}
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        self.loaded = False
        for title in {'f10', 'f10a_supplement', 'f10b_shareholder', 'f11_industry', 'f12_finance'}:
            if title == "f10b_shareholder":
                a = json.loads(json.loads(open('data/{}.json'.format(title), encoding='utf-8-sig').read())["msg"])
                for k in a:
                    a[k] = a[k].replace('"{', "{").replace('}"', "}").replace("\\\\", "\\") \
                        .replace("\\r", "").replace('\\"', '"')
                self.loaded_data[title] = a
            elif title == "f12_finance":
                a = json.loads(json.loads(open('data/{}.json'.format(title), encoding='utf-8-sig').read())["msg"])
                for k in a:
                    a[k] = a[k].replace(r'\"', '"').replace('"{', "{").replace('}"', "}")
                self.loaded_data[title] = a
            else:
                self.loaded_data[title] = json.loads(
                    json.loads(open('data/{}.json'.format(title), encoding='utf-8-sig').read())["msg"])
        self.loaded = True
        self.notify_console("data loaded...updated at {}".format(self.win_conf["updatetime"]))

    def enable_btn(self,id):
        self.router.browser.page().runJavaScript(
            "$('#{}').prop('disabled',false)".format(id))

    def notify_console(self, msg):
        print("notifyConsole: " + msg)
        self.router.browser.page().runJavaScript(
            "$('#console').prepend('<div class=\"text-align-left\">{}</div>')".format(msg))

    def notify_subwin(self, win, name):
        if win in self.subWindows:
            print("notifying {}; vm.items={}".format(win, self.loaded_data[win][name]))
            self.subWindows[win].chrome_widget.browser.page().runJavaScript(
                "vm.items={}".format(self.loaded_data[win][name]))

    @pyqtSlot(str, result=list)
    def resetConf(self, name):
        with open('pages/{}/conf/{}_bak.json'.format(name, name), encoding="utf-8") as json_file:
            with open('pages/{}/conf/{}.json'.format(name, name), 'w', encoding='utf-8') as f:
                f.write(json_file.read())

        return self.getConf(name)

    @pyqtSlot(str, list)
    def update(self, path, args_list):
        def _fetch():
            [self.notify_console(i.replace("\"", "").replace("'", "")) for i in fetch.fetch(path, args_list)]
            self.win_conf["updatetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.load_data()
            self.enable_btn("update")

        self.loaded = False
        threading.Thread(target=_fetch).start()

    @pyqtSlot(str, str)
    def nav(self, path, _from):
        print("from {} to {}".format(_from, path))
        self.router.nav(path)

    @pyqtSlot(str,int,int)
    def removeWindow(self,title,height,width):
        self.win_conf[title]["height"]=height
        self.win_conf[title]["width"]=width
        self.subWindows.pop(title)

    @pyqtSlot(str,result=str)
    def newWindow(self, title):
        if self.loaded and len(self.cur_name[0])>0:
            if title not in self.subWindows:
                h=self.win_conf[title]["height"] if "height" in self.win_conf[title] else 480
                w = self.win_conf[title]["width"] if "width" in self.win_conf[title] else 640
                self.subWindows[title] = subWindow.SubWindow(title,self.loaded_data[title][self.cur_name[0]],
                                                             rmFn=self.removeWindow,h=h,w=w)
                self.closeSig.connect(self.subWindows[title].closeEvent)
                self.toggleTopmostSig.connect(self.subWindows[title].toggle_stay_on_top)
                self.toggleTopmostSig.emit(self.win_conf["topmost"])
        else:
            return "数据加载:{}; tdx股名:{}".format(self.loaded,self.cur_name[0])
        return ""



    @pyqtSlot(str, list, result=bool)
    def saveConf(self, name, confList):

        with open('pages/{}/conf/{}.json'.format(name, name), 'w', encoding="utf-8-sig", errors="ignore") as f:
            json.dump({name: confList}, f, ensure_ascii=False, indent=4)

        if name != 'home': threading.Thread(target=self.genTemp[name]).start()
        return True

    @pyqtSlot(str, result=list)
    def getConf(self, name):
        with open('pages/{}/conf/{}.json'.format(name, name), encoding="utf-8-sig", errors="ignore") as json_file:
            return json.load(json_file)[name]

    @pyqtSlot(bool)
    def setboss(self, b):
        self.win_conf["boss"] = b

    @pyqtSlot()
    def apply_strat(self):
        def _strat():
            apply_strat(self.notify_console)
            self.enable_btn("apply_strat")
        threading.Thread(target=_strat).start()


class ChromeWidget(QWidget):
    def __init__(self, parent, cur_name):
        super(ChromeWidget, self).__init__(parent)
        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self.parent = parent
        self.browser.page().setWebChannel(self.channel)
        self.backend = Backend(Router(self.browser), cur_name)
        self.channel.registerObject('backend', self.backend)
        self.backend.router.nav('home')
        self.__layout()
        self.setFixedSize(930, 580)

    def __layout(self):
        self.vBox = QVBoxLayout()
        self.hBox = QVBoxLayout()
        self.hBox.addWidget(self.browser)
        self.vBox.addLayout(self.hBox)
        self.setLayout(self.vBox)
        self.hBox.setContentsMargins(0, 0, 0, 0)

        self.vBox.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    # win.toggle_stay_on_top(True)
    win.show()
    return app.exec_()

if __name__ == '__main__':
    import os

    # os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    sys.argv.append("--disable-web-security")
    sys.exit(main())
