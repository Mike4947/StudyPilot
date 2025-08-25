from PyQt5 import QtCore, QtGui, QtWidgets

class SubjectsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)

        row = QtWidgets.QHBoxLayout()
        self.name = QtWidgets.QLineEdit(); self.name.setPlaceholderText("Nom (ex: Math)")
        self.color = QtWidgets.QLineEdit("#3b82f6")
        self.add = QtWidgets.QPushButton("Ajouter")
        row.addWidget(self.name,1); row.addWidget(self.color); row.addWidget(self.add)
        v.addLayout(row)

        self.list = QtWidgets.QListWidget(); v.addWidget(self.list,1)

        self.data=None; self.saver=None
        self.add.clicked.connect(self.add_subject)

    def set_data(self,d): self.data=d
    def set_saver(self,fn): self.saver=fn
    def refresh(self):
        self.list.clear()
        for s in self.data.get("subjects", []):
            self.list.addItem(f"{s.get('name')}  ({s.get('id')})  {s.get('color')}")

    def add_subject(self):
        name = self.name.text().strip(); color = self.color.text().strip() or "#64748b"
        if not name: return
        sid = name.lower().replace(" ","-")
        subs = self.data.setdefault("subjects", [])
        if any(s.get("id")==sid for s in subs):
            QtWidgets.QMessageBox.warning(self,"Existe","Identifiant déjà utilisé."); return
        subs.append({"id":sid,"name":name,"color":color})
        self.name.clear()
        if self.saver: self.saver()
        self.refresh()
