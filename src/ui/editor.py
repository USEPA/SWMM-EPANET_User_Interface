# Based on example code from https://github.com/goldsborough/Writer-Tutorial

import os, sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

ICON_FOLDER = "icons/editor/"
MAX_RECENT_FILES = 8

class EditorWindow(QtGui.QMainWindow):
    def __init__(self, parent=None, session=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.file_name = ""
        self.changesSaved = True
        self.session = session
        self.initUI()
        if session:
            self.recent_scripts = self.create_recent_menus(self.menu_file, self.open_recent_script)

    def initToolbar(self):

        self.newAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "new.png")), "New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new script from scratch.")
        self.newAction.triggered.connect(self.new)

        self.runAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "play.png")), "Run", self)
        # self.playAction.setShortcut("Ctrl+N")
        self.runAction.setStatusTip("Run this script")
        self.runAction.triggered.connect(self.run)

        self.openAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "open.png")), "Open file", self)
        self.openAction.setStatusTip("Open existing script")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "save.png")), "Save", self)
        self.saveAction.setStatusTip("Save script")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.saveAsAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "save.png")), "Save As...", self)
        self.saveAsAction.setStatusTip("Save script as...")
        self.saveAsAction.triggered.connect(self.save_as)

        self.printAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "print.png")), "Print script", self)
        self.printAction.setStatusTip("Print script")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "preview.png")), "Page view", self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)

        self.cutAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "cut.png")), "Cut to clipboard", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "copy.png")), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "paste.png")), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "undo.png")), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "redo.png")), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.runAction)
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

    def set_font_size(self):
        cursor = self.text.textCursor()
        self.text.selectAll()
        self.text.setFontPointSize(self.fontSize.value())
        self.text.setTextCursor(cursor)

    def initFormatbar(self):

        self.fontBox = QtGui.QFontComboBox(self)
        self.fontBox.currentFontChanged.connect(lambda font: self.text.setFont(font))

        self.fontSize = QtGui.QSpinBox(self)

        # Will display " pt" after each value
        self.fontSize.setSuffix(" pt")

        self.fontSize.valueChanged.connect(self.set_font_size)

        self.fontSize.setValue(14)

        indentAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "indent.png")), "Indent Area", self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QtGui.QAction(QtGui.QIcon(os.path.join(ICON_FOLDER, "dedent.png")), "Unindent Area", self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        self.toolbar.addSeparator()

        self.toolbar.addAction(indentAction)
        self.toolbar.addAction(dedentAction)

        self.toolbar.addSeparator()

        self.toolbar.addWidget(self.fontBox)
        self.toolbar.addWidget(self.fontSize)


    def initMenubar(self):

        menubar = self.menuBar()

        self.menu_file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        # Add the most important actions to the menubar

        self.menu_file.addAction(self.runAction)
        self.menu_file.addAction(self.newAction)
        self.menu_file.addAction(self.openAction)
        self.menu_file.addAction(self.saveAction)
        self.menu_file.addAction(self.printAction)
        self.menu_file.addAction(self.previewAction)


        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)

        # Toggling actions for the various bars
        toolbarAction = QtGui.QAction("Toggle Toolbar", self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        statusbarAction = QtGui.QAction("Toggle Statusbar", self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        view.addAction(statusbarAction)

    def create_recent_menus(self, parent_menu, callback):
        """Create recent menus. All are invisible and have no text yet, that happens in update_recent."""
        menus = []
        parent_menu.addSeparator()
        for i in range(MAX_RECENT_FILES):
            action = QtGui.QAction(self, visible=False, triggered=callback)
            # if parent_menu is not self.menuScripting:
            #     action.setShortcut(QKeySequence("Ctrl+" + str(i+1)))
            menus.append(action)
            parent_menu.addAction(action)
        return menus

    def initUI(self):

        self.text = QtGui.QTextEdit(self)

        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.text.setTabStopWidth(33)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        self.setCentralWidget(self.text)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        self.text.textChanged.connect(self.changed)

        self.setGeometry(100, 100, 1030, 800)
        self.setWindowTitle("Script Editor")
        self.setWindowIcon(QtGui.QIcon(os.path.join(ICON_FOLDER, "icon.png")))
        try:
            import highlighting
            highlighting.PythonHighlighter(self.text.document())
        except Exception as ex_highlight:
            print(ex_highlight.message)
            pass

    def changed(self):
        self.changesSaved = False

    def closeEvent(self, event):
        if self.changesSaved:
            event.accept()
        else:
            popup = QtGui.QMessageBox(self)
            popup.setIcon(QtGui.QMessageBox.Warning)
            popup.setText("The script has been modified")
            popup.setInformativeText("Do you want to save your changes?")
            popup.setStandardButtons(QtGui.QMessageBox.Save |
                                     QtGui.QMessageBox.Cancel |
                                     QtGui.QMessageBox.Discard)
            popup.setDefaultButton(QtGui.QMessageBox.Save)
            answer = popup.exec_()
            if answer == QtGui.QMessageBox.Save:
                self.save()
            elif answer == QtGui.QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

    def context(self, pos):
        # Grab the cursor
        cursor = self.text.textCursor()
        event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse, QtCore.QPoint())
        self.text.contextMenuEvent(event)

    def toggleToolbar(self):
        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleStatusbar(self):
        state = self.statusbar.isVisible()

        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)

    def new(self):
        spawn = EditorWindow()
        spawn.show()

    def run(self):
        if self.session:
            self.save()
            self.session.script_run(self.file_name)

    def open(self):
        if self.session:
            file_name = self.session.script_browse_open()
        else:
            file_name = QtGui.QFileDialog.getOpenFileName(self, "Select script", ".", "(*.py)")
        self.open_file(file_name)

    def open_recent_script(self):
        action = self.sender()
        if action and action.data():
            self.open_file(action.data())

    def open_file(self, file_name):
        if file_name:
            with open(file_name, "rt") as open_file:
                self.text.setText(open_file.read())
            self.set_file_name(file_name)

    def save_as(self):
        self.save(True)

    def save(self, must_ask=False):
        # Open dialog if there is no file name yet or if Save As needs a new name
        file_name = self.file_name
        if must_ask or not file_name:
            if self.session:
                file_name = self.session.script_browse_save()
            else:
                file_name = QtGui.QFileDialog.getSaveFileName(self, "Save Script As...")

        if file_name:
            # Append extension if not there yet
            if not str(self.file_name).lower().endswith(".py"):
                self.file_name += ".py"

            with open(file_name, "wt") as save_file:
                save_file.write(self.text.toPlainText())
            self.set_file_name(file_name)

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.changesSaved = True
        self.setWindowTitle("Script Editor - " + self.file_name)

    def preview(self):
        # Open preview dialog
        preview = QtGui.QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))
        preview.exec_()

    def printHandler(self):
        # Open printing dialog
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):
        cursor = self.text.textCursor()
        # convert from zero to 1-indexed
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line, col))

    def indent(self):
        # Grab the cursor
        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:
            cursor.insertText("\t")

    def handleDedent(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):
        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    main = EditorWindow()
    main.show()

    sys.exit(app.exec_())

