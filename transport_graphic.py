from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
Form, Window = uic.loadUiType(u"maket\Transpotr_maket.ui")
app = QApplication([])
window = Window()
form = Form()


if __name__ == "__main__":
    form.setupUi(window)
    window.show()
    app.exec_()