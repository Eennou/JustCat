

if __name__ == "__main__":
    import sys
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebChannel import QWebChannel
    from playsound import playsound
    from threading import Thread, Event
    import os

    # import math


    app = None
    web = None
    bridge = None
    soundRunning = Event()

    def playsoundCustom(path):
        global soundRunning
        playsound(path)
        soundRunning.clear()


    class Bridge(QtCore.QObject):
        @QtCore.pyqtSlot()
        def purr(self):
            global soundRunning
            if not soundRunning.is_set():
                sound = Thread(target=playsoundCustom, daemon=True, args=(os.path.abspath(os.getcwd()).replace("\\", "/") + "/web/sound1.mp3",))
                soundRunning.set()
                sound.start()
                # playsound(os.path.abspath(os.getcwd()).replace("\\", "/") + "/web/sound1.mp3")

        @QtCore.pyqtSlot(str, result=str)
        def local_page(self, url):
            print(f"./web/{url}.html")
            with open(f"./web/{url}.html", "r") as file:
                html = file.read()
            return html

        @QtCore.pyqtSlot(str)
        def send_page(self, html):
            print(html)

    def local_page(url):
        print(f"./web/{url}")
        with open(f"./web/{url}", "r") as file:
            html = file.read()
        return html


    def closeApp():
        print("terminate")

    def CreateWindow():
        global web, app, bridge
        # sys.argv.append("--disable-web-security")
        app = QApplication(sys.argv)
        web = QWebEngineView()
        web.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        app.setApplicationName("Cat")
        app.setWindowIcon(QtGui.QIcon('web/logo1.png'))
        web.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        web.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # web.setWindowOpacity(0.8)
        web.page().setBackgroundColor(QtCore.Qt.GlobalColor.transparent)
        web.resize(240, 160)
        screen = app.primaryScreen()
        size = screen.size()
        web.move(size.width()-240, size.height()-160-40)
        web.setHtml(local_page("main.html"))
        web.show()

        # BRIDGE
        channel = QWebChannel(web.page())
        web.page().setWebChannel(channel)
        # web.addAction(QAction("Exit", shortcut=QtGui.QKeySequence("Ctrl+c"), triggered=lambda: closeApp))

        bridge = Bridge()
        channel.registerObject("bridge", bridge)


    CreateWindow()

    sys.exit(app.exec_())