"""
    Handle "Help" keypress and open help viewer to the correct topic.
"""
import os, sys
from PyQt4 import Qt, QtCore, QtGui


class HelpHandler(QtGui.QMainWindow):

    HELP_KEYS = [QtCore.Qt.Key_F1, QtCore.Qt.Key_Help]
    help_assistant_executable = "assistant.exe"
    help_assistant_arguments = ["-collectionFile", "helpfilename", "-enableRemoteControl"]
    help_process = QtCore.QProcess()

    @staticmethod
    def init_class(help_filename, assistant_executable_full_path=''):
        if not os.path.isfile(assistant_executable_full_path):
            assistant_executable_full_path = Qt.QLibraryInfo.location(Qt.QLibraryInfo.BinariesPath)
            if 'darwin' in sys.platform:
                assistant_executable_full_path += "/Assistant.app/Contents/MacOS/Assistant"
                ext = '.dylib'
            elif 'win' in sys.platform:
                assistant_executable_full_path += "/assistant.exe"
            else:  # Linux
                assistant_executable_full_path += "/assistant"

        HelpHandler.help_assistant_executable = assistant_executable_full_path
        HelpHandler.help_assistant_arguments[1] = help_filename

    def __init__(self, parent, help_topic):
        QtGui.QMainWindow.__init__(self, parent)
        self.help_topic = help_topic

    def show_help(self, help_topic=None):
        # open qt assistant for help
        if HelpHandler.help_process:
            if HelpHandler.help_process.state() == HelpHandler.help_process.NotRunning:
                HelpHandler.help_process.close()
                HelpHandler.help_process = None
        if not HelpHandler.help_process:
            HelpHandler.help_process = QtCore.QProcess()
            HelpHandler.help_process.start(HelpHandler.help_assistant_executable, HelpHandler.help_assistant_arguments)

        if not help_topic:
            help_topic = self.help_topic

        # Trim leading slashes and backslashes
        while help_topic.startswith('/') or help_topic.startswith('\\'):
            help_topic = help_topic[1:]

        # set to the right page
        ba = QtCore.QByteArray()
        ba.append("setSource qthelp://" + help_topic + '\n')
        HelpHandler.help_process.write(ba)

    def keyPressEvent(self, event):
        if event.key() in self.HELP_KEYS:
            self.show_help()
