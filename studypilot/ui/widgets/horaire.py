from PyQt5 import QtCore, QtGui, QtWidgets

PERIODS = ["P1","Pause","P2","Midi","P3","P4"]

class HoraireWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)

        top = QtWidgets.QHBoxLayout()
        self.date = QtWidgets.QDateEdit(QtCore.QDate.currentDate()); self.date.setCalendarPopup(True)
        self.spin = QtWidgets.QSpinBox(); self.spin.setRange(1,9); self.spin.setValue(1)
        self.btn = QtWidgets.QPushButton("Construire carte des jours")
        top.addWidget(QtWidgets.QLabel("Début:")); top.addWidget(self.date)
        top.addWidget(QtWidgets.QLabel("Jour:")); top.addWidget(self.spin)
        top.addWidget(self.btn); top.addStretch(1)
        v.addLayout(top)

        self.table = QtWidgets.QTableWidget(7,10)
        self.table.setHorizontalHeaderLabels(["", *[f"Jour {i}" for i in range(1,10)]])
        self.table.setVerticalHeaderLabels(["", *PERIODS])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.on_context)
        v.addWidget(self.table,1)

        self.data=None; self.saver=None
        self.btn.clicked.connect(self.build_map)

    def set_data(self, d): self.data=d
    def set_saver(self, fn): self.saver=fn
    def refresh(self):
        # fill horaire labels
        h = self.data.get("horaire", {})
        for r in range(1,7):
            for c in range(1,10):
                self.table.setItem(r,c, QtWidgets.QTableWidgetItem(""))
        for day, per in h.items():
            day = int(day)
            for period, slot in per.items():
                r = {"P1":1,"Pause":2,"P2":3,"Midi":4,"P3":5,"P4":6}.get(period,1)
                self.table.setItem(r, day, QtWidgets.QTableWidgetItem(slot.get("label","")))

    def build_map(self):
        from datetime import timedelta
        start = self.date.date().toPyDate()
        n = self.spin.value()
        m = {}
        d = start
        for _ in range(200):
            if d.weekday()<5:
                m[d.strftime("%Y-%m-%d")] = n
                n = 1 if n==9 else n+1
            d += timedelta(days=1)
        self.data["cycleMap"]=m
        if self.saver: self.saver()
        QtWidgets.QMessageBox.information(self,"OK","Carte des jours générée.")
        self.refresh()

    def on_context(self, pos):
        idx = self.table.indexAt(pos)
        if not idx.isValid(): return
        row,col = idx.row(), idx.column()
        if row==0 or col==0: return
        period = ["","P1","Pause","P2","Midi","P3","P4"][row]
        day = col

        menu = QtWidgets.QMenu(self)
        a1 = menu.addAction("Définir libellé du cours…")
        a2 = menu.addAction("Ajouter note récurrente (jour de cycle)…")
        act = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if act == a1:
            label, ok = QtWidgets.QInputDialog.getText(self, "Cours", "Libellé:")
            if not ok: return
            self.data.setdefault("horaire",{}).setdefault(str(day),{})[period]={"label":label,"subjectId":"default"}
            if self.saver: self.saver()
            self.refresh()
        elif act == a2:
            title, ok = QtWidgets.QInputDialog.getText(self, "Note récurrente", "Titre:")
            if not ok: return
            ev = {"id":QtCore.QUuid.createUuid().toString(),"type":"note","title":title,"subjectId":"default",
                  "date":QtCore.QDate.currentDate().toString("yyyy-MM-dd"),"period":"",
                  "recurrence":{"kind":"cycle","cycleDays":[day]},"done":False}
            self.data.setdefault("events",[]).append(ev)
            if self.saver: self.saver()
