# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Slot

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_BudgetUIBase

class BudgetUIBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_BudgetUIBase()
        self.ui.setupUi(self)
    @Slot()
    def onClick():
        print("Yeehaw")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BudgetUIBase()
    widget.show()
    sys.exit(app.exec())
