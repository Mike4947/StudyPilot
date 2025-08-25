from PyQt5 import QtCore, QtGui, QtWidgets

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        pix = QtGui.QPixmap(680, 320)
        pix.fill(QtCore.Qt.transparent)
        super().__init__(pix)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._progress = 0

    def drawContents(self, painter):
        r = self.rect()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # card
        path = QtGui.QPainterPath()
        rr = QtCore.QRectF(r.adjusted(16,16,-16,-16))
        path.addRoundedRect(rr, 24, 24)
        painter.fillPath(path, QtGui.QColor(21,26,33,240))
        # title
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold))
        painter.drawText(r.adjusted(40,36,-40,-40), QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop, "StudyPilot Local")
        painter.setPen(QtGui.QColor("#98a2b3"))
        painter.setFont(QtGui.QFont("Segoe UI", 10))
        painter.drawText(r.adjusted(40,72,-40,-40), QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop, "Chargement…")
        # progress
        bar = QtCore.QRect(40, r.height()-80, r.width()-80, 18)
        painter.setPen(QtGui.QPen(QtGui.QColor("#232a33"), 1))
        painter.setBrush(QtGui.QColor("#151a21"))
        painter.drawRoundedRect(QtCore.QRectF(bar), 9, 9)
        fillw = int((bar.width()-4) * self._progress/100.0)
        painter.fillRect(QtCore.QRect(bar.left()+2, bar.top()+2, fillw, bar.height()-4), QtGui.QColor("#3b82f6"))
        painter.setPen(QtGui.QColor("#e6eaf2"))
        painter.drawText(r.adjusted(40,0,-40,-28), QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom, f"{self._progress}%")

    def set_progress(self, v):
        self._progress = max(0, min(100, int(v)))
        self.repaint()
