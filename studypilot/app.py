import os, sys, json, time, platform, hashlib, secrets
from dataclasses import asdict
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.splash import SplashScreen
from .ui.login import LoginWindow
from .ui.mainwindow import MainWindow
from .model.storage import AppStorage
from .model.auth import AuthManager

APP_NAME = "StudyPilotLocal"

def resource_path(rel):
    base = os.path.dirname(__file__)
    return os.path.join(base, rel)

def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("StudyPilot Local")
    app.setOrganizationName("StudyPilot")
    app.setStyle("Fusion")

    # Global font
    font = QtGui.QFont("Segoe UI", 10)
    app.setFont(font)

    # Premium dark palette
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(15,18,22))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(21,26,33))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(25,31,39))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(21,26,33))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(59,130,246))
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

    # Splash
    splash = SplashScreen()
    splash.show()
    for i in range(1, 101, 7):
        splash.set_progress(i)
        QtWidgets.QApplication.processEvents()
        time.sleep(0.01)

    storage = AppStorage(APP_NAME)
    auth = AuthManager(storage)

    # Login
    login = LoginWindow(auth)
    splash.finish(login)
    login.show()

    def on_logged_in(username):
        # load user data and open main window
        mw = MainWindow(storage, username)
        mw.show()
        login.close()

    login.logged_in.connect(on_logged_in)

    sys.exit(app.exec_())
