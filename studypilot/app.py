import sys, time
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.splash import SplashScreen
from .ui.login import LoginWindow
from .ui.mainwindow import MainWindow
from .model.storage import AppStorage
from .model.auth import AuthManager

APP_NAME = "StudyPilotLocal"

def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("StudyPilot Local")
    app.setOrganizationName("StudyPilot")
    app.setStyle("Fusion")

    # Premium palette
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(15,18,22))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(21,26,33))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(25,31,39))
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(21,26,33))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor("#3b82f6"))
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

    # Optional QSS
    try:
        from importlib import resources
        qss = resources.read_text("studypilot.qss", "theme.qss")
        app.setStyleSheet(qss)
    except Exception:
        pass

    splash = SplashScreen()
    splash.show()
    for i in range(0, 101, 5):
        splash.set_progress(i)
        QtWidgets.QApplication.processEvents()
        time.sleep(0.01)

    storage = AppStorage(APP_NAME)
    auth = AuthManager(storage)

    login = LoginWindow(auth)
    splash.finish(login)
    login.show()

    def on_logged_in(username):
        win = MainWindow(storage, username)
        win.show()
        login.close()

    login.logged_in.connect(on_logged_in)
    sys.exit(app.exec_())
