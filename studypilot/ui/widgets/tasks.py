from PyQt5 import QtCore, QtGui, QtWidgets

class TasksWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)
        top = QtWidgets.QHBoxLayout()
        self.combo = QtWidgets.QComboBox(); self.combo.addItems(["Tous","Devoir","Examen"])
        self.clear = QtWidgets.QPushButton("Supprimer terminés")
        top.addWidget(QtWidgets.QLabel("Filtre:")); top.addWidget(self.combo); top.addStretch(1); top.addWidget(self.clear)
        v.addLayout(top)

        self.list = QtWidgets.QListWidget(); v.addWidget(self.list,1)
        self.data=None; self.saver=None
        self.combo.currentIndexChanged.connect(self.refresh)
        self.clear.clicked.connect(self.clear_done)

    def set_data(self, d): self.data=d
    def set_saver(self, fn): self.saver=fn
    def refresh(self):
        self.list.clear()
        t = self.combo.currentText().lower()
        for ev in self.data.get("events", []):
            if ev.get("type") in ["devoir","examen"]:
                if t!="tous" and ev.get("type")!=t: continue
                self.list.addItem(f"{ev.get('type').upper()} • {ev.get('title')} • {ev.get('date')} {ev.get('period','')}")

    def clear_done(self):
        self.data["events"] = [e for e in self.data.get("events",[]) if not e.get("done")]
        if self.saver: self.saver()
        self.refresh()
