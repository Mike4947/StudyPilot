from PyQt5 import QtCore, QtGui, QtWidgets

class LoginWindow(QtWidgets.QWidget):
    logged_in = QtCore.pyqtSignal(str)
    def __init__(self, auth):
        super().__init__()
        self.auth = auth
        self.setWindowTitle("StudyPilot – Connexion")
        self.resize(560, 380)
        self.setWindowFlag(QtCore.Qt.Window)

        v = QtWidgets.QVBoxLayout(self); v.setContentsMargins(24,24,24,24); v.setSpacing(16)
        title = QtWidgets.QLabel("<h2>🔐 StudyPilot</h2><div style='color:#98a2b3'>Master Password</div>")
        v.addWidget(title)

        form = QtWidgets.QFormLayout()
        self.user = QtWidgets.QComboBox()
        form.addRow("Utilisateur", self.user)
        self.pw = QtWidgets.QLineEdit(); self.pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pw.returnPressed.connect(self.try_login)
        form.addRow("Mot de passe", self.pw)
        v.addLayout(form)

        # Bottom bar: left = Créer utilisateur, right = Ouvrir session
        bottom = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Créer un utilisateur")
        bottom.addWidget(self.btn_add)
        bottom.addStretch(1)
        self.btn_login = QtWidgets.QPushButton("Ouvrir la session")
        bottom.addWidget(self.btn_login)
        v.addLayout(bottom)

        # Ultra-bottom row: hint + supprimer
        ultra = QtWidgets.QHBoxLayout()
        ultra.addWidget(QtWidgets.QLabel("<span style='color:#98a2b3'>Plusieurs utilisateurs supportés</span>"))
        ultra.addStretch(1)
        self.btn_del = QtWidgets.QPushButton("Supprimer utilisateur"); self.btn_del.setFlat(True)
        ultra.addWidget(self.btn_del)
        v.addLayout(ultra)

        self.btn_login.clicked.connect(self.try_login)
        self.btn_add.clicked.connect(self.add_user)
        self.btn_del.clicked.connect(self.del_user)

        self.refresh_users()

    def refresh_users(self):
        names = self.auth.list_users()
        self.user.clear(); self.user.addItems(names)
        if not names:
            QtWidgets.QMessageBox.information(self, "Bienvenue", "Aucun utilisateur. Crée le premier compte.")
            self.add_user()

    def add_user(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Nouvel utilisateur", "Nom d'utilisateur:")
        if not ok or not name.strip(): return
        pwd, ok2 = QtWidgets.QInputDialog.getText(self, "Mot de passe", "Choisis un mot de passe:", QtWidgets.QLineEdit.Password)
        if not ok2 or not pwd: return
        try:
            self.auth.create_user(name.strip(), pwd)
            self.refresh_users(); self.user.setCurrentText(name.strip())
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

    def del_user(self):
        u = self.user.currentText()
        if not u: return
        if QtWidgets.QMessageBox.question(self, "Confirmer", f"Supprimer l'utilisateur “{u}” ?")==QtWidgets.QMessageBox.Yes:
            try:
                self.auth.delete_user(u); self.refresh_users()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

    def try_login(self):
        u = self.user.currentText(); p = self.pw.text()
        if not u or not p:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Renseigne utilisateur et mot de passe.")
            return
        if self.auth.verify_password(u, p):
            self.logged_in.emit(u)
        else:
            QtWidgets.QMessageBox.critical(self, "Refusé", "Mot de passe invalide.")
