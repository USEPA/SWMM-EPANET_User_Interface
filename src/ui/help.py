"""
    Handle "Help" keypress and open help viewer to the correct topic.
"""
import os, sys
from PyQt4 import Qt, QtCore, QtGui


class HelpHandler(QtCore.QObject):

    HELP_KEYS = [QtCore.Qt.Key_F1, QtCore.Qt.Key_Help]
    help_assistant_executable = "assistant.exe"
    help_assistant_arguments = ["-collectionFile", "helpfilename", "-enableRemoteControl"]
    help_process = QtCore.QProcess()

    @staticmethod
    def init_class(help_filename, assistant_executable_full_path=''):
        if not os.path.isfile(assistant_executable_full_path):
            if assistant_executable_full_path:  # also search above specified folder
                search_dir = os.path.dirname(assistant_executable_full_path)
                while search_dir and not os.path.isfile(os.path.join(search_dir, HelpHandler.help_assistant_executable)):
                    # print(HelpHandler.help_assistant_executable + " Not found in " + search_dir)
                    next_search_dir = os.path.dirname(search_dir)
                    if next_search_dir == search_dir:
                        break
                    search_dir = next_search_dir
                if search_dir:
                    assistant_executable_full_path = os.path.join(search_dir, HelpHandler.help_assistant_executable)
            if not os.path.isfile(assistant_executable_full_path):
                search_dir = os.path.dirname(os.path.abspath(__file__))
                while search_dir and not os.path.isfile(os.path.join(search_dir, HelpHandler.help_assistant_executable)):
                    # print(HelpHandler.help_assistant_executable + " Not found in " + search_dir)
                    next_search_dir = os.path.dirname(search_dir)
                    if next_search_dir == search_dir:
                        break
                    search_dir = next_search_dir
                if search_dir:
                    assistant_executable_full_path = os.path.join(search_dir, HelpHandler.help_assistant_executable)
            if not os.path.isfile(assistant_executable_full_path):
                assistant_executable_full_path = Qt.QLibraryInfo.location(Qt.QLibraryInfo.BinariesPath)
                if 'darwin' in sys.platform:
                    assistant_executable_full_path += "/Assistant.app/Contents/MacOS/Assistant"
                    ext = '.dylib'
                elif 'win' in sys.platform:
                    assistant_executable_full_path += "/assistant.exe"
                else:  # Linux
                    assistant_executable_full_path += "/assistant"

        print "HelpHandler.help_assistant_executable = " + assistant_executable_full_path
        HelpHandler.help_assistant_executable = assistant_executable_full_path

        if not os.path.isfile(help_filename):
            search_dir = os.path.dirname(help_filename)
            help_file_name_only = help_filename[len(search_dir):]
            while search_dir and not os.path.isfile(os.path.join(search_dir, help_file_name_only)):
                # print help_file_name_only + " Not found in " + search_dir
                next_search_dir = os.path.dirname(search_dir)
                if next_search_dir == search_dir:
                    break
                search_dir = next_search_dir
            if search_dir:
                help_filename = os.path.join(search_dir, help_file_name_only)

        print "HelpHandler.help_assistant_arguments[1] = " + help_filename
        HelpHandler.help_assistant_arguments[1] = help_filename

    def __init__(self, listen_here_for_help_key, help_topic=None):
        QtCore.QObject.__init__(self)
        """Create a HelpHandler that responds to Help key events on the Qt window listen_here_for_help_key"""
        self.listen_here_for_help_key = listen_here_for_help_key
        if listen_here_for_help_key:
            listen_here_for_help_key.installEventFilter(self)
            if help_topic:
                listen_here_for_help_key.help_topic = help_topic

    def show_help(self, help_topic=None):
        # open qt assistant for help
        if HelpHandler.help_process:
            if HelpHandler.help_process.state() == HelpHandler.help_process.NotRunning:
                HelpHandler.help_process.close()
                HelpHandler.help_process = None
        if not HelpHandler.help_process:
            HelpHandler.help_process = QtCore.QProcess()
            HelpHandler.help_process.start(HelpHandler.help_assistant_executable, HelpHandler.help_assistant_arguments)

        # If there is a help_topic specified as an argument, use it.
        # Otherwise if self.listen_here_for_help_key.help_topic is specified, use that topic.
        if not help_topic and hasattr(self.listen_here_for_help_key, "help_topic"):
            help_topic = self.listen_here_for_help_key.help_topic

        # If we found a topic, open it, otherwise help is already open from above, just leave it open.
        if help_topic:
            # Trim leading slashes and backslashes
            while help_topic.startswith('/') or help_topic.startswith('\\'):
                help_topic = help_topic[1:]

            # set to the right page
            help_command = QtCore.QByteArray()
            help_command.append("setSource qthelp://" + help_topic + '\n')
            HelpHandler.help_process.write(help_command)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in self.HELP_KEYS:
                self.show_help()
                return True
        return False
