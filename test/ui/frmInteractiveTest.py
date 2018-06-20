import sys
import PyQt5.Qt as Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QDialog, QListView, QPushButton, QVBoxLayout, QApplication


class frmInteractiveTest(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._parent = parent
        self.resize(400, 800)

        self.list_view = QListView()
        self.model = QtGui.QStandardItemModel()
        self.ok_button = QPushButton("OK")
        self.skip_button = QPushButton("Skip")

        self.ok_button.clicked.connect(self.clicked_ok)
        self.skip_button.clicked.connect(self.clicked_skip)

        layout = QVBoxLayout()

        layout.addWidget(self.list_view, 1)
        layout.addWidget(self.ok_button, 0)
        layout.addWidget(self.skip_button, 0)
        self.setLayout(layout)
        self.OK = False

    def set_list(self, list_items):
        self.model = QtGui.QStandardItemModel()

        for item_text in list_items:
            item = QtGui.QStandardItem(item_text)
            item.setCheckState(Qt.Qt.Unchecked)
            item.setCheckable(True)
            self.model.appendRow(item)
        self.list_view.setModel(self.model)

    def clicked_ok(self):
        self.OK = True
        self.close()

    def clicked_skip(self):
        self.OK = False
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainApp = frmInteractiveTest()
    MainApp.show()
    sys.exit(app.exec_())
