import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmCrossSectionDesigner import Ui_frmCrossSection


class frmCrossSection(QtGui.QMainWindow, Ui_frmCrossSection):


    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.listWidget.currentItemChanged.connect(self.listWidget_currentItemChanged)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.project.Control()
        section = project.find_section("CONTROLS")
        # self.txtControls.setPlainText(str(section.get_text()))
        self.listWidget.addItems(('Rectangular', 'Trapezoidal', 'Triangular', 'Parabolic', 'Power',
                                  'Irregular', 'Circular', 'Force Main', 'Filled Circular',
                                  'Closed Rectangular', 'Horizontal Elliptical', 'Vertical Elliptical',
                                  'Arch', 'Rectangular Triangular', 'Rectangular Round', 'Modified Baskethandle',
                                  'Egg', 'Horseshoe', 'Gothic', 'Catenary', 'Semi-Elliptical', 'Baskethandle',
                                  'Semi-Circular', 'Custom', 'Dummy'))
        self.listWidget.item(0).setIcon(QtGui.QIcon("../swmmimages/1rect.png"))
        self.listWidget.item(1).setIcon(QtGui.QIcon("../swmmimages/2trap.png"))
        self.listWidget.item(2).setIcon(QtGui.QIcon("../swmmimages/3tri.png"))
        self.listWidget.item(3).setIcon(QtGui.QIcon("../swmmimages/4para.png"))
        self.listWidget.item(4).setIcon(QtGui.QIcon("../swmmimages/5power.png"))
        self.listWidget.item(5).setIcon(QtGui.QIcon("../swmmimages/6irreg.png"))
        self.listWidget.item(6).setIcon(QtGui.QIcon("../swmmimages/7circ.png"))
        self.listWidget.item(7).setIcon(QtGui.QIcon("../swmmimages/8force.png"))
        self.listWidget.item(8).setIcon(QtGui.QIcon("../swmmimages/9filled.png"))
        self.listWidget.item(9).setIcon(QtGui.QIcon("../swmmimages/10closed.png"))
        self.listWidget.item(10).setIcon(QtGui.QIcon("../swmmimages/11horiz.png"))
        self.listWidget.item(11).setIcon(QtGui.QIcon("../swmmimages/12vert.png"))
        self.listWidget.item(12).setIcon(QtGui.QIcon("../swmmimages/13arch.png"))
        self.listWidget.item(13).setIcon(QtGui.QIcon("../swmmimages/14recttri.png"))
        self.listWidget.item(14).setIcon(QtGui.QIcon("../swmmimages/15rectround.png"))
        self.listWidget.item(15).setIcon(QtGui.QIcon("../swmmimages/16basket.png"))
        self.listWidget.item(16).setIcon(QtGui.QIcon("../swmmimages/17egg.png"))
        self.listWidget.item(17).setIcon(QtGui.QIcon("../swmmimages/18horse.png"))
        self.listWidget.item(18).setIcon(QtGui.QIcon("../swmmimages/19goth.png"))
        self.listWidget.item(19).setIcon(QtGui.QIcon("../swmmimages/20cat.png"))
        self.listWidget.item(20).setIcon(QtGui.QIcon("../swmmimages/21semi.png"))
        self.listWidget.item(21).setIcon(QtGui.QIcon("../swmmimages/22bask.png"))
        self.listWidget.item(22).setIcon(QtGui.QIcon("../swmmimages/23semi.png"))
        self.listWidget.item(23).setIcon(QtGui.QIcon("../swmmimages/24custom.png"))
        self.listWidget.item(24).setIcon(QtGui.QIcon("../swmmimages/25na.png"))

        self.listWidget_currentItemChanged()

    def cmdOK_Clicked(self):
        # will need to do some validating, see dxsect.pas
        section = self._parent.project.find_section("CONTROLS")
        section.set_text(str(self.txtControls.toPlainText()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def listWidget_currentItemChanged(self):

        cur = self.listWidget.currentItem()
        current_selection = ""
        if cur:
            current_selection = str(cur.text())

        units = 1

        self.lblSpin.setVisible(True)
        self.sbxNumber.setVisible(True)
        self.lblText1.setVisible(True)
        self.txt1.setVisible(True)
        self.lblText2.setVisible(True)
        self.lblText3.setVisible(True)
        self.lblText4.setVisible(True)
        self.txt2.setVisible(True)
        self.txt3.setVisible(True)
        self.txt4.setVisible(True)
        self.lblDimensions.setVisible(True)
        if units == 1:
            self.lblDimensions.setText('Dimensions are feet unless otherwise stated.')
        else:
            self.lblDimensions.setText('Dimensions are meters unless otherwise stated.')

        self.lblFootnote.setVisible(False)
        self.lblCombo.setVisible(False)
        self.cboCombo.setVisible(False)
        self.btnDialog.setVisible(False)

  # // Minor and major axis lengths for standard ellipsoid pipes
  # // in both inches and mm
  # EllipseMinorAxisIN: array[1..23] of Integer =
  # (14,19,22,24,27,29,32,34,38,43,48,53,58,63,68,72,77,82,87,92,97,106,116);
  #
  # EllipseMajorAxisIN: array[1..23] of Integer =
  # (23,30,34,38,42,45,49,53,60,68,76,83,91,98,106,113,121,128,136,143,151,166,180);
  #
  # EllipseMinorAxisMM: array[1..23] of Integer =
  # (356,483,559,610,686,737,813,864,965,1092,1219,1346,1473,1600,
  #  1727,1829,1956,2083,2210,2337,2464,2692,2946);
  #
  # EllipseMajorAxisMM: array[1..23] of Integer =
  # (584,762,864,965,1067,1143,1245,1346,1524,1727,1930,2108,2311,
  #  2489,2692,2870,3073,3251,3454,3632,3835,4216,4572);
  #
  #  ArchHeightIN: array[1..102] of String =
  #  // Concrete
  #  ('11','13.5','15.5','18','22.5','26.625','31.3125','36','40','45','54','62',
  #   '72','77.5','87.125','96.875','106.5',
  #  // Corrugated Steel - 2-2/3 x 1/2" corrugations
  #   '13','15','18','20','24','29','33','38','43','47','52','57',
  #  // Corrugated Steel - 3 x 1" corrugations
  #   '31','36','41','46','51','55','59','63','67','71','75','79','83','87','91',
  #  // Structural Plate - 18" Corner Radius
  #   '55','57','59','61','63','65','67','69','71','73','75','77','79','81','83',
  #   '85','87','89','91','93','95','97','100','101','103','105','107','109',
  #   '111','113','115','118','119','121',
  #  // Structural Plate - 31" Corner Radius
  #   '112','114','116','118','120','122','124','126','128','130','132','134',
  #   '136','138','140','142','144','146','148','150','152','154','156','158');
  #
  #   ArchWidthIN: array[1..102] of String =
  #  // Concrete
  #   ('18','22','26','28.5','36.25','43.75','51.125','58.5','65','73','88','102',
  #   '115','122','138','154','168.75',
  #  // Corrugated Steel - 2-2/3 x 1/2" corrugations
  #    '17','21','24','28','35','42','49','57','64','71','77','83',
  #  // Corrugated Steel - 3 x 1" corrugations
  #    '40','46','53','60','66','73','81','87','95','103','112','117','128',
  #    '137','142',
  #  // Structural Plate - 18" Corner Radius
  #    '73','76','81','84','87','92','95','98','103','106','112','114','117',
  #    '123','128','131','137','139','142','148','150','152','154','161','167',
  #    '169','171','178','184','186','188','190','197','199',
  #  // Structural Plate - 31" Corner Radius
  #    '159','162','168','170','173','179','184','187','190','195','198','204',
  #    '206','209','215','217','223','225','231','234','236','239','245','247');


        if current_selection == 'Rectangular':
            XType = 'RECT_OPEN'
            self.lblText2.setText('Bottom Width')
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Open rectangular channel. Sidewalls can be removed for 2-D modeling.')
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            self.cboCombo.clear()
            self.cboCombo.addItems(('None','One','Both'))
            self.lblCombo.setText('Sidewalls Removed')
        elif current_selection == 'Trapezoidal':
            XType = 'TRAPEZOIDAL'
            self.lblText2.setText('Bottom Width')
            self.lblText3.setText('Left Slope')
            self.lblText4.setText('Right Slope')
            self.lblBottom.setText('Open trapezoidal channel. Slopes are horizontal / vertical.')
        elif current_selection == 'Triangular':
            XType = 'TRIANGULAR'
            self.lblText2.setText('Top Width')
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Open triangular channel.')
        elif current_selection == 'Parabolic':
            XType = 'PARABOLIC'
            self.lblText2.setText('Top Width')
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Open parabolic channel where depth varies with top width squared.')
        elif current_selection == 'Power':
            XType = 'POWER'
            self.lblText2.setText('Top Width')
            self.lblText3.setText('Power')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Open channel where depth varies with top width to some power.')
        elif current_selection == 'Irregular':
            XType = 'IRREGULAR'
            self.lblSpin.setVisible(False)
            self.sbxNumber.setVisible(False)
            self.lblText1.setVisible(False)
            self.txt1.setVisible(False)
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Open irregular natural channel described by transect coordinates.')
            self.lblCombo.setText('Transect Name')
            self.cboCombo.clear()
            # self.cboCombo.addItems('None','One','Both') # need to set from available transects
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            self.btnDialog.setVisible(True)
        elif current_selection == 'Circular':
            XType = 'CIRCULAR'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Standard circular pipe.')
        elif current_selection == 'Force Main':
            XType = 'FORCE_MAIN'
            self.lblText2.setText('Roughness*')
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Circular pipe with a special friction loss equation for pressurized flow.')
                # if SameText(Project.Options.Data[FORCE_MAIN_EQN_INDEX], 'H-W') then
                #   ForceMainNote.Caption := '*Hazen-Williams C-factor'
                # else if Uglobals.UnitSystem = usUS
                # then ForceMainNote.Caption := '*Darcy-Weisbach roughness height (inches)'
                # else ForceMainNote.Caption := '*Darcy-Weisbach roughness height (mm)'
            self.lblFootnote.setVisible(True)
        elif current_selection == 'Filled Circular':
            XType = 'FILLED_CIRCULAR'
            self.lblText2.setText('Filled Depth')
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Circular pipe partly filled with sediment.')
        elif current_selection == 'Closed Rectangular':
            XType = 'RECT_CLOSED'
            self.lblText2.setText('Bottom Width')
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Closed rectangular box conduit.')
        elif current_selection == 'Horizontal Elliptical':
            XType = 'HORIZ_ELLIPSE'
            self.lblText2.setText('Maximum Width')
            self.lblText3.setText('Size Code')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            if units == 1:
                self.lblCombo.setText('Standard Sizes (inches)')
            else:
                self.lblCombo.setText('Standard Sizes (mm)')
            self.cboCombo.clear()
            self.cboCombo.addItems(('Custom','XX','XX'))
            self.lblBottom.setText('Closed horizontal elliptical pipe. Select a standard size or "Custom" to enter a custom height and width.')
        elif current_selection == 'Vertical Elliptical':
            XType = 'VERT_ELLIPSE'
            self.lblText2.setText('Maximum Width')
            self.lblText3.setText('Size Code')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            if units == 1:
                self.lblCombo.setText('Standard Sizes (inches)')
            else:
                self.lblCombo.setText('Standard Sizes (mm)')
            self.cboCombo.clear()
            self.cboCombo.addItems(('Custom','XX','XX'))
            self.lblBottom.setText('Closed vertical elliptical pipe. Select a standard size or "Custom" to enter a custom height and width.')
        elif current_selection == 'Arch':
            XType = 'ARCH'
            self.lblText2.setText('Maximum Width')
            self.lblText3.setText('Size Code')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            if units == 1:
                self.lblCombo.setText('Standard Sizes (inches)')
            else:
                self.lblCombo.setText('Standard Sizes (mm)')
            self.cboCombo.clear()
            self.cboCombo.addItems(('Custom','XX','XX'))
            self.lblBottom.setText('Closed arch pipe. Select a standard size or "Custom" to enter a custom height and width.')
        elif current_selection == 'Rectangular Triangular':
            XType = 'RECT_TRIANGULAR'
            self.lblText2.setText('Top Width')
            self.lblText3.setText('Triangle Height')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Closed rectangular top with triangular bottom.')
        elif current_selection == 'Rectangular Round':
            XType = 'RECT_ROUND'
            self.lblText2.setText('Top Width')
            self.lblText3.setText('Bottom Radius')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Closed rectangular top with circular bottom.')
        elif current_selection == 'Modified Baskethandle':
            XType = 'MODBASKETHANDLE'
            self.lblText2.setText('Bottom Width')
            self.lblText3.setText('Top Radius')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Rectangular bottom with closed circular top.')
        elif current_selection == 'Egg':
            XType = 'EGG'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Classic Phillips Standard Egg sewer shape.')
        elif current_selection == 'Horseshoe':
            XType = 'HORSESHOE'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Classic Boston Horseshoe sewer shape.')
        elif current_selection == 'Gothic':
            XType = 'GOTHIC'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Classic Gothic sewer shape.')
        elif current_selection == 'Catenary':
            XType = 'CATENARY'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Classic Catenary sewer shape (i.e., inverted egg).')
        elif current_selection == 'Semi-Elliptical':
            XType = 'SEMIELLIPTICAL'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Classic Louisville Semi-Elliptical sewer shape.')
        elif current_selection == 'Baskethandle':
            XType = 'BASKETHANDLE'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Classic Baskethandle sewer shape.')
        elif current_selection == 'Semi-Circular':
            XType = 'SEMICIRCULAR'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('Classic Semi-Circular sewer shape.')
        elif current_selection == 'Custom':
            XType = 'CUSTOM'
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblCombo.setText('Shape Curve Name')
            self.cboCombo.clear()
            # self.cboCombo.addItems('Custom','XX','XX') # need to set from available transects
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            self.btnDialog.setVisible(True)
            self.lblBottom.setText('Closed custom shape described by a user-supplied shape curve.')
        elif current_selection == 'Dummy':
            XType = 'DUMMY'
            self.lblSpin.setVisible(False)
            self.sbxNumber.setVisible(False)
            self.lblText1.setVisible(False)
            self.txt1.setVisible(False)
            self.lblText2.setVisible(False)
            self.txt2.setVisible(False)
            self.lblText3.setVisible(False)
            self.txt3.setVisible(False)
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblBottom.setText('There are no parameters for a dummy cross-section.')
            self.lblDimensions.setVisible(False)
