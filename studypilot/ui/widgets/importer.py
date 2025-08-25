from PyQt5 import QtCore, QtGui, QtWidgets

class ImportWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)
        row = QtWidgets.QHBoxLayout()
        self.ics = QtWidgets.QPushButton("Importer ICS")
        self.csv = QtWidgets.QPushButton("Importer CSV Horaire")
        row.addWidget(self.ics); row.addWidget(self.csv); row.addStretch(1)
        v.addLayout(row)
        v.addStretch(1)
        self.data=None; self.saver=None
        self.ics.clicked.connect(self.import_ics)
        self.csv.clicked.connect(self.import_csv)

    def set_data(self,d): self.data=d
    def set_saver(self,fn): self.saver=fn
    def refresh(self): pass

    def import_ics(self):
        path,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Choisir ICS", "", "ICS (*.ics)")
        if not path: return
        try:
            with open(path,"r",encoding="utf-8",errors="ignore") as f:
                lines=f.read().splitlines()
            cur={}; count=0
            for L in lines:
                L=L.strip()
                if L=="BEGIN:VEVENT": cur={}
                elif L.startswith("SUMMARY:"): cur["summary"]=L[8:]
                elif L.startswith("DTSTART"): cur["dt"]=L.split(":")[1]
                elif L=="END:VEVENT":
                    if "summary" in cur and "dt" in cur:
                        d=cur["dt"][:8]; y,m,d2=d[:4],d[4:6],d[6:8]
                        ev={"id":QtCore.QUuid.createUuid().toString(),"type":"evenement","title":cur["summary"],
                            "subjectId":"default","date":f"{y}-{m}-{d2}","period":"","recurrence":{"kind":"none"},"done":False}
                        self.data.setdefault("events",[]).append(ev); count+=1
            if self.saver: self.saver()
            QtWidgets.QMessageBox.information(self,"OK",f"{count} évènement(s) importé(s).")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self,"Erreur",str(e))

    def import_csv(self):
        path,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Choisir CSV", "", "CSV (*.csv)")
        if not path: return
        try:
            with open(path,"r",encoding="utf-8",errors="ignore") as f:
                rows=[r.strip() for r in f.read().splitlines() if r.strip()]
            if rows and rows[0].lower().startswith("daycycle"): rows=rows[1:]
            for r in rows:
                dayStr, period, label, *rest = [c.strip() for c in r.split(",")]
                day = int(dayStr)
                self.data.setdefault("horaire",{}).setdefault(str(day),{})[period]={"label":label,"subjectId":"default"}
            if self.saver: self.saver()
            QtWidgets.QMessageBox.information(self,"OK","Horaire importé.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self,"Erreur",str(e))
