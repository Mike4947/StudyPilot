import json
from datetime import date, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets
from .widgets.agenda import AgendaWidget
from .widgets.horaire import HoraireWidget
from .widgets.tasks import TasksWidget
from .widgets.subjects import SubjectsWidget
from .widgets.tools import ToolsWidget
from .widgets.importer import ImportWidget
from .widgets.settings import SettingsWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, storage, username:str):
        super().__init__()
        self.storage = storage
        self.username = username
        self.setWindowTitle(f"StudyPilot – {username}")
        self.resize(1280, 820)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabs.setDocumentMode(True)
        self.setCentralWidget(self.tabs)

        # Build tabs
        self.agenda = AgendaWidget(self)
        self.horaire = HoraireWidget(self)
        self.tasks = TasksWidget(self)
        self.subjects = SubjectsWidget(self)
        self.tools = ToolsWidget(self)
        self.importer = ImportWidget(self)
        self.settings = SettingsWidget(self)

        self.tabs.addTab(self.agenda, "Agenda")
        self.tabs.addTab(self.horaire, "Horaire 1–9")
        self.tabs.addTab(self.tasks, "Devoirs & Examens")
        self.tabs.addTab(self.subjects, "Matières")
        self.tabs.addTab(self.tools, "Outils")
        self.tabs.addTab(self.importer, "Importer")
        self.tabs.addTab(self.settings, "Paramètres")

        self.load_all()
        self.statusBar().showMessage("Prêt")

    # Storage helpers
    def load_all(self):
        self.data = self.storage.load_user_data(self.username)
        # Wire data to tabs
        for w in [self.agenda, self.horaire, self.tasks, self.subjects, self.tools, self.importer, self.settings]:
            w.set_data(self.data)
            w.set_saver(self.save)
        self.agenda.refresh()
        self.horaire.refresh()
        self.tasks.refresh()
        self.subjects.refresh()
        self.tools.refresh()
        self.importer.refresh()
        self.settings.refresh()

    def save(self):
        self.storage.save_user_data(self.username, self.data)
        self.statusBar().showMessage("Sauvegardé", 2000)
