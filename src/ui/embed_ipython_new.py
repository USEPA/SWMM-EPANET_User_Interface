"""
Author: Tim Rae
The following solution is posted:
http://stackoverflow.com/questions/11513132/embedding-ipython-qt-console-in-a-pyqt-application
The accepted answer by @ChrisB is fine for IPython version 0.13, but it doesn't work with
newer versions. From the examples section of the IPython tree on github, this is the way to
do it in 1.1.0, which has the feature that the console and kernel are in the same process.

Here is an example, based on the official one, which gives a convenience class that can be
easily plugged into an application. It's setup to work with pyqt4 and IPython 1.1.0 on Python 2.7:
"""
# Set the QT API to PyQt4
import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from PyQt4.QtGui import *
# Import the console machinery from ipython
from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.qt.inprocess import QtInProcessKernelManager
from IPython.lib import guisupport
from PyQt4 import QtCore

class QIPythonWidget(RichIPythonWidget):
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self,customBanner=None,*args,**kwargs):
        if customBanner!=None: self.banner=customBanner
        super(QIPythonWidget, self).__init__(*args,**kwargs)
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel_manager.kernel.gui = 'qt4'
        #self.kernel_manager.kernel.shell.push(kwargs)
        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()

        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()
            guisupport.get_app_qt4().exit()            
        self.exit_requested.connect(stop)

    def pushVariables(self,variableDict):
        """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
        self.kernel_manager.kernel.shell.push(variableDict)
    def clearTerminal(self):
        """ Clears the terminal """
        self._control.clear()    
    def printText(self,text):
        """ Prints some plain text to the console """
        self._append_plain_text(text)        
    def executeCommand(self,command):
        """ Execute a command in the frame of the console widget """
        self._execute(command,False)


class EmbedIPython(QWidget):
    """ Main GUI Widget including a button and IPython Console widget inside vertical layout """
    def __init__(self, parent=None, **kwargs):
        super(EmbedIPython, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.button = QPushButton('Another widget')
        ipyConsole = QIPythonWidget(customBanner="Welcome to the embedded ipython console\n",**kwargs)
        layout.addWidget(self.button)
        layout.addWidget(ipyConsole)        
        # This allows the variable foo and method print_process_id to be accessed from the ipython console
        #ipyConsole.pushVariables({"foo":43,"print_process_id":print_process_id})
        ipyConsole.pushVariables(kwargs)
        ipyConsole.printText("The variable 'foo' and the method 'print_process_id()' are available. Use the 'whos' command for information.")

def print_process_id():
    print 'Process ID is:', os.getpid()        

def main():
    app  = QApplication([])
    widget = EmbedIPython()
    widget.show()
    app.exec_()    

if __name__ == '__main__':
    main()
