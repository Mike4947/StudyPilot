from datetime import date, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets

PERIODS = ["P1","Pause","P2","Midi","P3","P4"]

class AgendaWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)

        top = QtWidgets.QHBoxLayout()
        self.prev = QtWidgets.QPushButton("◀ Semaine -1")
        self.next = QtWidgets.QPushButton("+1 Semaine ▶")
        self.label = QtWidgets.QLabel("Semaine")
        top.addWidget(self.prev); top.addWidget(self.label,1); top.addWidget(self.next)
        v.addLayout(top)

        self.table = QtWidgets.QTableWidget(7, 6)  # header row + 6 rows for periods
        self.table.setHorizontalHeaderLabels(["","Lun","Mar","Mer","Jeu","Ven"])
        self.table.setVerticalHeaderLabels(["", *PERIODS])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.on_context)
        v.addWidget(self.table,1)

        self.monday = self._monday(date.today())
        self.data = None
        self.saver = None

        self.prev.clicked.connect(lambda: self.shift(-7))
        self.next.clicked.connect(lambda: self.shift(+7))

    def set_data(self, data): self.data = data
    def set_saver(self, fn): self.saver = fn
    def refresh(self):
        m = self.monday
        self.label.setText(f"Semaine du {m.strftime('%d/%m/%Y')}")
        # headers
        for c in range(1,6):
            d = m + timedelta(days=c-1)
            self.table.setItem(0,c, QtWidgets.QTableWidgetItem(d.strftime("%a %d/%m")))
        # clear
        for r in range(1,7):
            for c in range(1,6):
                self.table.setItem(r,c, QtWidgets.QTableWidgetItem(""))
        # fill
        for ev in self.data.get("events", []):
            s = ev.get("date","")
            try:
                y,mn,dd = map(int, s.split("-"))
                dt = date(y,mn,dd)
            except: 
                continue
            if not (m <= dt <= m+timedelta(days=4)): 
                continue
            col = (dt-m).days+1
            row = {"P1":1,"Pause":2,"P2":3,"Midi":4,"P3":5,"P4":6}.get(ev.get("period",""),1)
            old = self.table.item(row,col).text() if self.table.item(row,col) else ""
            txt = f"{ev.get('type')}: {ev.get('title')}"
            self.table.setItem(row,col, QtWidgets.QTableWidgetItem((old+"\n"+txt).strip()))

    def _monday(self, d): return d - timedelta(days=d.weekday())
    def shift(self, n): self.monday += timedelta(days=n); self.refresh()

    def on_context(self, pos):
        idx = self.table.indexAt(pos)
        if not idx.isValid(): return
        row, col = idx.row(), idx.column()
        if row==0 or col==0: return
        m = self.monday
        dt = m + timedelta(days=col-1)
        period = ["","P1","Pause","P2","Midi","P3","P4"][row]

        menu = QtWidgets.QMenu(self)
        for t in ["note","absence","devoir","examen"]:
            act = menu.addAction(f"Ajouter {t}")
            act.triggered.connect(lambda _, tt=t: self.add_event(dt, period, tt))
        menu.exec_(self.table.viewport().mapToGlobal(pos))

    def add_event(self, dt, period, typ):
        if self.data is None: return
        title, ok = QtWidgets.QInputDialog.getText(self, f"Nouveau {typ}", "Titre:")
        if not ok: return
        ev = {"id": QtCore.QUuid.createUuid().toString(),
              "type": typ, "title": title, "subjectId": "default",
              "date": dt.strftime("%Y-%m-%d"), "period": period,
              "recurrence":{"kind":"none"}, "done": False}
        self.data.setdefault("events", []).append(ev)
        if self.saver: self.saver()
        self.refresh()
