import sys
import PyQt4.Qt as Qt
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore


class frmInteractiveTest(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self._parent = parent
        self.resize(400, 800)

        self.list_view = QtGui.QListView()
        self.model = QtGui.QStandardItemModel()
        self.ok_button = QtGui.QPushButton("OK")
        self.skip_button = QtGui.QPushButton("Skip")

        self.ok_button.clicked.connect(self.clicked_ok)
        self.skip_button.clicked.connect(self.clicked_skip)

        layout = QtGui.QVBoxLayout()

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
    app = QtGui.QApplication(sys.argv)
    MainApp = frmInteractiveTest()
    MainApp.show()
    sys.exit(app.exec_())