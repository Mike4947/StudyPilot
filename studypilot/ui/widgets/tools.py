from PyQt5 import QtCore, QtGui, QtWidgets

class ToolsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)

        # Pomodoro
        box = QtWidgets.QGroupBox("Pomodoro"); vbox = QtWidgets.QVBoxLayout(box)
        form = QtWidgets.QFormLayout()
        self.work = QtWidgets.QSpinBox(); self.work.setRange(5,120); self.work.setValue(25)
        self.breakm = QtWidgets.QSpinBox(); self.breakm.setRange(1,60); self.breakm.setValue(5)
        self.display = QtWidgets.QLabel("25:00")
        self.start = QtWidgets.QPushButton("Démarrer"); self.stop = QtWidgets.QPushButton("Stop")
        form.addRow("Travail (min)", self.work)
        form.addRow("Pause (min)", self.breakm)
        form.addRow("Affichage", self.display)
        hb = QtWidgets.QHBoxLayout(); hb.addWidget(self.start); hb.addWidget(self.stop); form.addRow(hb)
        vbox.addLayout(form)
        v.addWidget(box)

        self.timer = QtCore.QTimer(self); self.timer.timeout.connect(self.tick)
        self.left=0; self.phase="work"
        self.start.clicked.connect(self.go)
        self.stop.clicked.connect(lambda: self.timer.stop())

        # Moyenne
        box2 = QtWidgets.QGroupBox("Moyenne pondérée"); v2 = QtWidgets.QVBoxLayout(box2)
        self.table = QtWidgets.QTableWidget(3,3); self.table.setHorizontalHeaderLabels(["Nom","Note (%)","Poids (%)"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.calc = QtWidgets.QPushButton("Calculer"); self.out = QtWidgets.QLabel("—")
        v2.addWidget(self.table); v2.addWidget(self.calc); v2.addWidget(self.out)
        self.calc.clicked.connect(self.compute)
        v.addWidget(box2)

        # Révision
        box3 = QtWidgets.QGroupBox("Liste de révision"); v3 = QtWidgets.QVBoxLayout(box3)
        row = QtWidgets.QHBoxLayout(); self.inp = QtWidgets.QLineEdit(); self.add = QtWidgets.QPushButton("Ajouter"); row.addWidget(self.inp,1); row.addWidget(self.add)
        self.list = QtWidgets.QListWidget()
        v3.addLayout(row); v3.addWidget(self.list)
        self.add.clicked.connect(self.add_item)
        v.addWidget(box3,1)

        self.data=None; self.saver=None

    def set_data(self,d): self.data=d
    def set_saver(self,fn): self.saver=fn
    def refresh(self): pass

    def go(self):
        self.left=self.work.value()*60; self.phase="work"; self.timer.start(1000); self.update_display()
    def tick(self):
        self.left -= 1
        if self.left<=0:
            if self.phase=="work":
                QtWidgets.QMessageBox.information(self,"Pause","Pause !")
                self.left=self.breakm.value()*60; self.phase="break"
            else:
                QtWidgets.QMessageBox.information(self,"Reprise","C'est reparti !")
                self.timer.stop()
        self.update_display()
    def update_display(self):
        m=self.left//60; s=self.left%60; self.display.setText(f"{m:02d}:{s:02d}")

    def compute(self):
        rows=self.table.rowCount(); total=0.0; weight=0.0
        for r in range(rows):
            try:
                n=float(self.table.item(r,1).text()) if self.table.item(r,1) else 0.0
                p=float(self.table.item(r,2).text()) if self.table.item(r,2) else 0.0
                total += n*(p/100.0); weight += p
            except: pass
        if weight>0:
            self.out.setText(f"Moyenne: {total/(weight/100.0):.2f} %")
        else:
            self.out.setText("Ajoute des lignes valides.")

    def add_item(self):
        t=self.inp.text().strip()
        if not t: return
        self.list.addItem(t); self.inp.clear()
