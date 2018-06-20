import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.swmm.options.files
from ui.SWMM.frmInterfaceFilesDesigner import Ui_frmInterfaceFiles


class frmInterfaceFiles(QMainWindow, Ui_frmInterfaceFiles):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/simulationoptions_interface.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

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
