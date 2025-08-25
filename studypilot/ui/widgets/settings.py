import json
from PyQt5 import QtCore, QtGui, QtWidgets

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)
        row = QtWidgets.QHBoxLayout()
        self.exp = QtWidgets.QPushButton("Exporter JSON")
        self.imp = QtWidgets.QPushButton("Importer JSON")
        row.addWidget(self.exp); row.addWidget(self.imp); row.addStretch(1)
        v.addLayout(row)
        v.addStretch(1)
        self.data=None; self.saver=None
        self.exp.clicked.connect(self.export_json)
        self.imp.clicked.connect(self.import_json)

    def set_data(self,d): self.data=d
    def set_saver(self,fn): self.saver=fn
    def refresh(self): pass

    def export_json(self):
        path,_ = QtWidgets.QFileDialog.getSaveFileName(self,"Exporter","studypilot_backup.json","JSON (*.json)")
        if not path: return
        with open(path,"w",encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def import_json(self):
        path,_ = QtWidgets.QFileDialog.getOpenFileName(self,"Importer","","JSON (*.json)")
        if not path: return
        try:
            with open(path,"r",encoding="utf-8") as f:
                self.data.clear(); self.data.update(json.load(f))
            if self.saver: self.saver()
            QtWidgets.QMessageBox.information(self,"OK","Import réussi.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self,"Erreur",str(e))
