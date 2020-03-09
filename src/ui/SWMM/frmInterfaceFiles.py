import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import core.swmm.options.files
from ui.SWMM.frmInterfaceFilesDesigner import Ui_frmInterfaceFiles


class frmInterfaceFiles(QMainWindow, Ui_frmInterfaceFiles):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/simulationoptions_interface.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.cmdUseRainfall.clicked.connect(self.cmdUseRainfall_Clicked)
        self.cmdSaveRainfall.clicked.connect(self.cmdSaveRainfall_Clicked)
        self.cmdUseRunoff.clicked.connect(self.cmdUseRunoff_Clicked)
        self.cmdSaveRunoff.clicked.connect(self.cmdSaveRunoff_Clicked)
        self.cmdUseHotstart.clicked.connect(self.cmdUseHotstart_Clicked)
        self.cmdSaveHotstart.clicked.connect(self.cmdSaveHotstart_Clicked)
        self.cmdUseRDII.clicked.connect(self.cmdUseRDII_Clicked)
        self.cmdSaveRDII.clicked.connect(self.cmdSaveRDII_Clicked)
        self.cmdUseInflows.clicked.connect(self.cmdUseInflows_Clicked)
        self.cmdSaveInflows.clicked.connect(self.cmdSaveInflows_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmInterfaceFiles_geometry") and
                main_form.program_settings.value("Geometry/" + "frmInterfaceFiles_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmInterfaceFiles_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmInterfaceFiles_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        # section = core.swmm.options.files.Files()
        section = project.files
        self.txtUseRainfall.setText(frmInterfaceFiles.blank_if_none(section.use_rainfall))
        self.txtSaveRainfall.setText(frmInterfaceFiles.blank_if_none(section.save_rainfall))
        self.txtUseRunoff.setText(frmInterfaceFiles.blank_if_none(section.use_runoff))
        self.txtSaveRunoff.setText(frmInterfaceFiles.blank_if_none(section.save_runoff))
        self.txtUseHotstart.setText(frmInterfaceFiles.blank_if_none(section.use_hotstart))
        self.txtSaveHotstart.setText(frmInterfaceFiles.blank_if_none(section.save_hotstart))
        self.txtUseRDII.setText(frmInterfaceFiles.blank_if_none(section.use_rdii))
        self.txtSaveRDII.setText(frmInterfaceFiles.blank_if_none(section.save_rdii))
        self.txtUseInflows.setText(frmInterfaceFiles.blank_if_none(section.use_inflows))
        self.txtSaveOutflows.setText(frmInterfaceFiles.blank_if_none(section.save_outflows))

    def cmdOK_Clicked(self):
        section = self._main_form.project.files

        orig_use_rainfall = section.use_rainfall
        orig_save_rainfall = section.save_rainfall
        orig_use_runoff = section.use_runoff
        orig_save_runoff = section.save_runoff
        orig_use_hotstart = section.use_hotstart
        orig_save_hotstart = section.save_hotstart
        orig_use_rdii = section.use_rdii
        orig_save_rdii = section.save_rdii
        orig_use_inflows = section.use_inflows
        orig_save_outflows = section.save_outflows

        section.use_rainfall = frmInterfaceFiles.none_if_blank(self.txtUseRainfall.text())
        section.save_rainfall = frmInterfaceFiles.none_if_blank(self.txtSaveRainfall.text())
        section.use_runoff = frmInterfaceFiles.none_if_blank(self.txtUseRunoff.text())
        section.save_runoff = frmInterfaceFiles.none_if_blank(self.txtSaveRunoff.text())
        section.use_hotstart = frmInterfaceFiles.none_if_blank(self.txtUseHotstart.text())
        section.save_hotstart = frmInterfaceFiles.none_if_blank(self.txtSaveHotstart.text())
        section.use_rdii = frmInterfaceFiles.none_if_blank(self.txtUseRDII.text())
        section.save_rdii = frmInterfaceFiles.none_if_blank(self.txtSaveRDII.text())
        section.use_inflows = frmInterfaceFiles.none_if_blank(self.txtUseInflows.text())
        section.save_outflows = frmInterfaceFiles.none_if_blank(self.txtSaveOutflows.text())

        if section.use_rainfall:
            if section.use_rainfall[0] != '"':
                section.use_rainfall = '"' + section.use_rainfall + '"'
        if section.save_rainfall:
            if section.save_rainfall[0] != '"':
                section.save_rainfall = '"' + section.save_rainfall + '"'
        if section.use_runoff:
            if section.use_runoff[0] != '"':
                section.use_runoff = '"' + section.use_runoff + '"'
        if section.save_runoff:
            if section.save_runoff[0] != '"':
                section.save_runoff = '"' + section.save_runoff + '"'
        if section.use_hotstart:
            if section.use_hotstart[0] != '"':
                section.use_hotstart = '"' + section.use_hotstart + '"'
        if section.save_hotstart:
            if section.save_hotstart[0] != '"':
                section.save_hotstart = '"' + section.save_hotstart + '"'
        if section.use_rdii:
            if section.use_rdii[0] != '"':
                section.use_rdii = '"' + section.use_rdii + '"'
        if section.use_inflows:
            if section.use_inflows[0] != '"':
                section.use_inflows = '"' + section.use_inflows + '"'
        if section.save_outflows:
            if section.save_outflows[0] != '"':
                section.save_outflows = '"' + section.save_outflows + '"'
        if section.save_rdii:
            if section.save_rdii[0] != '"':
                section.save_rdii = '"' + section.save_rdii + '"'

        if orig_use_rainfall != section.use_rainfall or \
            orig_save_rainfall != section.save_rainfall or \
            orig_use_runoff != section.use_runoff or \
            orig_save_runoff != section.save_runoff or \
            orig_use_hotstart != section.use_hotstart or \
            orig_save_hotstart != section.save_hotstart or \
            orig_use_rdii != section.use_rdii or \
            orig_save_rdii != section.save_rdii or \
            orig_use_inflows != section.use_inflows or \
            orig_save_outflows != section.save_outflows:
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmInterfaceFiles_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmInterfaceFiles_state", self.saveState())
        self.close()


    @staticmethod
    def blank_if_none(txt):
        if not txt:
            return ''
        return str(txt)

    @staticmethod
    def none_if_blank(txt):
        if txt:
            txt = txt.strip()
        if txt:
            return txt
        else:
            return None

    def cmdCancel_Clicked(self):
        self.close()

    def cmdUseRainfall_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Rainfall Interface File", '',
                                                      "Rainfall files (*.RFF);;All files (*.*)")
        if file_name:
            self.txtUseRainfall.setText(file_name)

    def cmdSaveRainfall_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Rainfall Interface File", '',
                                                      "Rainfall files (*.RFF);;All files (*.*)")
        if file_name:
            self.txtSaveRainfall.setText(file_name)

    def cmdUseRunoff_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Runoff Interface File", '',
                                                       "Runoff files (*.ROF);;All files (*.*)")
        if file_name:
            self.txtUseRunoff.setText(file_name)

    def cmdSaveRunoff_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Runoff Interface File", '',
                                                       "Runoff files (*.ROF);;All files (*.*)")
        if file_name:
            self.txtSaveRunoff.setText(file_name)

    def cmdUseHotstart_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Hotstart Interface File", '',
                                                       "Hotstart files (*.HSF);;All files (*.*)")
        if file_name:
            self.txtUseHotstart.setText(file_name)

    def cmdSaveHotstart_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Hotstart Interface File", '',
                                                       "Hotstart files (*.HSF);;All files (*.*)")
        if file_name:
            self.txtSaveHotstart.setText(file_name)

    def cmdUseRDII_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a RDII Interface File", '',
                                                       "RDII files (*.TXT);;All files (*.*)")
        if file_name:
            self.txtUseRDII.setText(file_name)

    def cmdSaveRDII_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a RDII Interface File", '',
                                                       "RDII files (*.TXT);;All files (*.*)")
        if file_name:
            self.txtSaveRDII.setText(file_name)

    def cmdUseInflows_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select an Inflow Interface File", '',
                                                       "Routing files (*.TXT);;All files (*.*)")
        if file_name:
            self.txtUseInflows.setText(file_name)

    def cmdSaveInflows_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select an Outflow Interface File", '',
                                                       "Routing files (*.TXT);;All files (*.*)")
        if file_name:
            self.txtSaveInflows.setText(file_name)
