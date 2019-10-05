from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
app = QApplication([])
window = QWidget()
window.showFullScreen()
layout = QVBoxLayout()

def buttonClicked(self):
    os.system(cmd)
    QtCore.QCoreApplication.instance().quit()
    btn = QtGui.QPushButton('Yes', self)
    btn.clicked.connect(self.buttonClicked)


layout.addWidget(QPushButton('Einzahlen'))
layout.addWidget(QPushButton('Auszahlen'))

window.setLayout(layout)
window.show()
app.exec_()
