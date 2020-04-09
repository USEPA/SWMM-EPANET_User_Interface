import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from frmDetailsDesigner import Ui_frmDetails
from ui.help import HelpHandler


class frmDetails(QMainWindow, Ui_frmDetails):

    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/projectmenu.htm"
        self.setupUi(self)
        self._main_form = main_form
        self.lstCategory.clicked.connect(self.display_section)
        self.lstCategory.currentItemChanged.connect(self.display_section)
        self.set_from(main_form.project)
        # self.tableWidget.setColumnWidth(0, self.width()-232)

    def set_from(self, project):
        # add items to list
        project_writer = self._main_form.project_writer_type()
        # project_string = self.as_text(project)
        project_string = project_writer.as_text(project)
        index = 0
        while index < len(project_string):
            index = project_string.find('[', index)
            if index == -1:
                break
            end_index = project_string.find(']', index+1)
            if end_index == -1:
                break
            list_item = project_string[index:end_index+1]
            if list_item == "[MAP]":
                break
            self.lstCategory.addItem(list_item)
            index += 1
        self.lstCategory.setCurrentRow(0)
        self.display_section()
        pass

    def display_section(self):
        project_writer = self._main_form.project_writer_type()
        project_string = project_writer.as_text(self._main_form.project)

        selected_text = self.lstCategory.currentItem().text()

        index = project_string.find(selected_text, 0)
        end_index = project_string.find('[', index + 1)
        section_text = project_string[index:end_index]
        section_text = section_text.replace("\t"," ")

        index = 0
        row_list = []
        header_text = ""
        while index < len(section_text):
            index = section_text.find('\n', index)
            if index == -1:
                break
            end_index = section_text.find('\n', index+1)
            if end_index == -1:
                break
            list_item = section_text[index+1:end_index]
            if list_item[0:2] == ";;":
                if len(header_text) == 0:
                    header_text = list_item[2:]
            elif len(list_item) > 0:
                row_list.append(list_item)
            index += 1

        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(len(row_list))

        header_labels = ["  " + header_text]
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        # self.tableWidget.setColumnWidth(0, self.width()-232)
        self.tableWidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        for r in range(0, len(row_list)):
            self.tableWidget.setItem(r , 0 ,QTableWidgetItem(row_list[r]))

        pass

