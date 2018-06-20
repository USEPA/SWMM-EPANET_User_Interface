import sys
import PyQt5.Qt as Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QDialog, QTreeWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QTreeWidgetItem, QApplication


class frmTreeViewUITest(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._parent = parent
        self.resize(400, 800)
        self.setWindowTitle('UI Tests, check if passed')

        # Create Tree widget
        self.tree = QTreeWidget()
        self.model_tests = []
        self.model_actions = []
        self.tree.setHeaderHidden(True)

        # Create TextEdit for tester comment section
        self.label = QLabel()
        self.notes = QTextEdit()

        # Create Ok and skip button
        self.ok_button = QPushButton("OK")
        self.skip_button = QPushButton("Skip")
        self.ok_button.clicked.connect(self.clicked_ok)
        self.skip_button.clicked.connect(self.clicked_skip)

        # Set lay out
        layout = QVBoxLayout()
        layout.addWidget(self.tree, 1)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.notes, 1)
        layout.addWidget(self.ok_button, 0)
        layout.addWidget(self.skip_button, 0)
        self.setLayout(layout)
        self.OK = False
        self.label.setText('Tester Comments:')
        self.tree.setFixedHeight(600)
        self.notes.setFixedHeight(100)

    def set_tree(self, parent_list, child_list, num_actions):
        test_num = 0
        action_start = 0
        action_end = num_actions[test_num] # First set = actions[0-4]

        if not parent_list:
            parent_list = ['Test']

        for parent_text in parent_list:
            parent_ = QTreeWidgetItem(self.tree)
            parent_.setText(0,parent_text)
            parent_.setFlags(parent_.flags() |
                             QtCore.Qt.ItemIsTristate |
                             QtCore.Qt.ItemIsUserCheckable)
            self.model_tests.append(parent_)
            test_num +=1
            if test_num > 1:
                action_start = action_end
                action_end = action_start + num_actions[test_num-1]

            for child_text in child_list[action_start:action_end]:
                child_ = QTreeWidgetItem(parent_)
                child_.setFlags(child_.flags() | QtCore.Qt.ItemIsUserCheckable)
                child_.setText(0, child_text)
                child_.setCheckState(0, QtCore.Qt.Unchecked)
                self.model_actions.append(child_)
        self.tree.expandAll()

    def clicked_ok(self):
        self.OK = True
        self.close()

    def clicked_skip(self):
        self.OK = False
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainApp = frmTreeViewUITest()
    MainApp.show()
    sys.exit(app.exec_())
