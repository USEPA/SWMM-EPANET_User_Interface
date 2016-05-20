import sys
import PyQt4.Qt as Qt
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore


class frmTreeViewUITest(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self._parent = parent
        self.resize(400, 800)
        self.setWindowTitle('Test SWMM UI, check if passed')

        # Create Tree widget
        self.tree = QtGui.QTreeWidget()
        self.tree.setHeaderHidden(True)

        # Create Ok and skip button
        self.ok_button = QtGui.QPushButton("OK")
        self.skip_button = QtGui.QPushButton("Skip")
        self.ok_button.clicked.connect(self.clicked_ok)
        self.skip_button.clicked.connect(self.clicked_skip)

        # Set lay out
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tree, 1)
        layout.addWidget(self.ok_button, 0)
        layout.addWidget(self.skip_button, 0)
        self.setLayout(layout)
        self.OK = False

    def set_list(self, parent_list, child_list, num_actions):
        test_num = 0
        action_start = 0
        action_end = num_actions[test_num] # First set = actions[0-4]

        for parent_text in parent_list:
            parent_ = QtGui.QTreeWidgetItem(self.tree)
            parent_.setText(0,parent_text)
            parent_.setFlags(parent_.flags() |
                             QtCore.Qt.ItemIsTristate |
                             QtCore.Qt.ItemIsUserCheckable)
            test_num +=1
            if test_num > 1:
                action_start = action_end
                action_end = action_start + num_actions[test_num-1]

            for child_text in child_list[action_start:action_end]:
                child_ = QtGui.QTreeWidgetItem(parent_)
                child_.setFlags(child_.flags() | QtCore.Qt.ItemIsUserCheckable)
                child_.setText(0, child_text)
                child_.setCheckState(0, QtCore.Qt.Unchecked)

    def clicked_ok(self):
        self.OK = True
        self.close()

    def clicked_skip(self):
        self.OK = False
        self.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainApp = frmTreeViewUITest()
    MainApp.show()
    sys.exit(app.exec_())