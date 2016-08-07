import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.hydraulics
import core.swmm.hydraulics.link
import core.swmm.options.dynamic_wave
from ui.SWMM.frmCrossSectionDesigner import Ui_frmCrossSection
from ui.SWMM.frmTransect import frmTransect
from ui.SWMM.frmCurveEditor import frmCurveEditor
from core.swmm.curves import CurveType


class frmCrossSection(QtGui.QMainWindow, Ui_frmCrossSection):

    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/cross_sectioneditordialog.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnDialog, QtCore.SIGNAL("clicked()"), self.btnDialog_Clicked)
        self.listWidget.currentItemChanged.connect(self.listWidget_currentItemChanged)
        self.cboCombo.currentIndexChanged.connect(self.cboCombo_currentIndexChanged)
        self.set_from(main_form.project)
        self._main_form = main_form
        self.link_name = ''
        self.ellipse_minor_axis_in = (14,19,22,24,27,29,32,34,38,43,48,53,58,63,68,72,77,82,87,92,97,106,116)
        self.ellipse_major_axis_in = (23,30,34,38,42,45,49,53,60,68,76,83,91,98,106,113,121,128,136,143,151,166,180)
        self.ellipse_minor_axis_mm = (356,483,559,610,686,737,813,864,965,1092,1219,1346,1473,1600,1727,1829,1956,2083,
                                     2210,2337,2464,2692,2946)
        self.ellipse_major_axis_mm = (584,762,864,965,1067,1143,1245,1346,1524,1727,1930,2108,2311,2489,2692,2870,3073,
                                     3251,3454,3632,3835,4216,4572)

        self.arch_type = ('Concrete','Concrete','Concrete','Concrete','Concrete','Concrete','Concrete','Concrete',
                          'Concrete','Concrete','Concrete','Concrete','Concrete','Concrete','Concrete','Concrete',
                          'Concrete',
                          'Corrugated Steel - 2-2/3 x 1/2" Corrugation','Corrugated Steel - 2-2/3 x 1/2" Corrugation',
                          'Corrugated Steel - 2-2/3 x 1/2" Corrugation','Corrugated Steel - 2-2/3 x 1/2" Corrugation',
                          'Corrugated Steel - 2-2/3 x 1/2" Corrugation','Corrugated Steel - 2-2/3 x 1/2" Corrugation',
                          'Corrugated Steel - 2-2/3 x 1/2" Corrugation','Corrugated Steel - 2-2/3 x 1/2" Corrugation',
                          'Corrugated Steel - 2-2/3 x 1/2" Corrugation','Corrugated Steel - 2-2/3 x 1/2" Corrugation',
                          'Corrugated Steel - 2-2/3 x 1/2" Corrugation','Corrugated Steel - 2-2/3 x 1/2" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation','Corrugated Steel - 3 x 1" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation','Corrugated Steel - 3 x 1" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation','Corrugated Steel - 3 x 1" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation','Corrugated Steel - 3 x 1" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation','Corrugated Steel - 3 x 1" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation','Corrugated Steel - 3 x 1" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation','Corrugated Steel - 3 x 1" Corrugation',
                          'Corrugated Steel - 3 x 1" Corrugation',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 18" Corner Radius','Structural Plate - 18" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius',
                          'Structural Plate - 31" Corner Radius','Structural Plate - 31" Corner Radius')
        self.arch_height_in = ('11','13.5','15.5','18','22.5','26.625','31.3125','36','40','45','54','62',
                               '72','77.5','87.125','96.875','106.5','13','15','18','20','24','29','33','38',
                               '43','47','52','57','31','36','41','46','51','55','59','63','67','71','75','79',
                               '83','87','91','55','57','59','61','63','65','67','69','71','73','75','77','79',
                               '81','83','85','87','89','91','93','95','97','100','101','103','105','107','109',
                               '111','113','115','118','119','121','112','114','116','118','120','122','124','126',
                               '128','130','132','134','136','138','140','142','144','146','148','150','152','154',
                               '156','158')
        self.arch_width_in = ('18','22','26','28.5','36.25','43.75','51.125','58.5','65','73','88','102','115','122',
                              '138','154','168.75','17','21','24','28','35','42','49','57','64','71','77','83','40',
                              '46','53','60','66','73','81','87','95','103','112','117','128','137','142',
                              '73','76','81','84','87','92','95','98','103','106','112','114','117','123','128','131',
                              '137','139','142','148','150','152','154','161','167','169','171','178','184','186',
                              '188','190','197','199','159','162','168','170','173','179','184','187','190','195',
                              '198','204','206','209','215','217','223','225','231','234','236','239','245','247')
        # set for first link for now
        self.set_link(main_form.project, '1')

    def set_link(self, project, link_name):
        # section = core.swmm.project.CrossSection()
        section = project.find_section("XSECTIONS")
        link_list = section.value[0:]
        # assume we want to edit the first one
        self.link_name = link_name
        for value in link_list:
            if value.link == link_name:
                # this is the link we want to edit
                for list_index in range(0,self.listWidget.count()):
                    list_item = self.listWidget.item(list_index)
                    if str(list_item.text()).upper() == value.shape.name:
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Force Main' and value.shape.name == 'FORCE_MAIN':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Filled Circular' and value.shape.name == 'FILLED_CIRCULAR':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Closed Rectangular' and value.shape.name == 'RECT_CLOSED':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Rectangular' and value.shape.name == 'RECT_OPEN':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Horizontal Elliptical' and value.shape.name == 'HORIZ_ELLIPSE':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Vertical Elliptical' and value.shape.name == 'VERT_ELLIPSE':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Rectangular Triangular' and value.shape.name == 'RECT_TRIANGULAR':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Rectangular Round' and value.shape.name == 'RECT_ROUND':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Modified Baskethandle' and value.shape.name == 'MODBASKETHANDLE':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Semi-Elliptical' and value.shape.name == 'SEMIELLIPTICAL':
                        self.listWidget.setCurrentItem(list_item)
                    elif str(list_item.text()) == 'Semi-Circular' and value.shape.name == 'SEMICIRCULAR':
                        self.listWidget.setCurrentItem(list_item)
                self.sbxNumber.setValue(int(value.barrels))
                self.txt1.setText(value.geometry1)
                self.txt2.setText(value.geometry2)
                self.txt3.setText(value.geometry3)
                self.txt4.setText(value.geometry4)

                # for rect_open sidewalls, set geom3 to 0,1,2 for None, One, Both
                if value.shape.name == 'RECTANGULAR':
                    self.cboCombo.setCurrentIndex(int(value.geometry3))

                # for horizontal and vertical elliptical and arch, combo gets standard sizes
                if value.shape.name == 'HORIZ_ELLIPSE':
                    self.cboCombo.setCurrentIndex(int(value.geometry3))
                if value.shape.name == 'VERT_ELLIPSE':
                    self.cboCombo.setCurrentIndex(int(value.geometry3))
                if value.shape.name == 'ARCH':
                    self.cboCombo.setCurrentIndex(int(value.geometry3))

                if value.shape.name == 'IRREGULAR':
                    # for irregular, combo needs transect names, dialog opens transect buttons
                    for index in range(0,self.cboCombo.count):
                        if value.transect == self.cboCombo.itemText(index):
                            self.cboCombo.setCurrentIndex(index)

                if value.shape.name == 'CUSTOM':
                    # for custom, combo needs shape curves, dialog opens shape curve editor
                    for index in range(0,self.cboCombo.count):
                        if value.curve == self.cboCombo.itemText(index):
                            self.cboCombo.setCurrentIndex(index)

                # section.culvert_code not used in ui


    def set_from(self, project):
        # section = core.swmm.project.CrossSection()
        self.listWidget.addItems(('Rectangular', 'Trapezoidal', 'Triangular', 'Parabolic', 'Power',
                                  'Irregular', 'Circular', 'Force Main', 'Filled Circular',
                                  'Closed Rectangular', 'Horizontal Elliptical', 'Vertical Elliptical',
                                  'Arch', 'Rectangular Triangular', 'Rectangular Round', 'Modified Baskethandle',
                                  'Egg', 'Horseshoe', 'Gothic', 'Catenary', 'Semi-Elliptical', 'Baskethandle',
                                  'Semi-Circular', 'Custom', 'Dummy'))
        self.listWidget.item(0).setIcon(QtGui.QIcon("./swmmimages/1rect.png"))
        self.listWidget.item(1).setIcon(QtGui.QIcon("./swmmimages/2trap.png"))
        self.listWidget.item(2).setIcon(QtGui.QIcon("./swmmimages/3tri.png"))
        self.listWidget.item(3).setIcon(QtGui.QIcon("./swmmimages/4para.png"))
        self.listWidget.item(4).setIcon(QtGui.QIcon("./swmmimages/5power.png"))
        self.listWidget.item(5).setIcon(QtGui.QIcon("./swmmimages/6irreg.png"))
        self.listWidget.item(6).setIcon(QtGui.QIcon("./swmmimages/7circ.png"))
        self.listWidget.item(7).setIcon(QtGui.QIcon("./swmmimages/8force.png"))
        self.listWidget.item(8).setIcon(QtGui.QIcon("./swmmimages/9filled.png"))
        self.listWidget.item(9).setIcon(QtGui.QIcon("./swmmimages/10closed.png"))
        self.listWidget.item(10).setIcon(QtGui.QIcon("./swmmimages/11horiz.png"))
        self.listWidget.item(11).setIcon(QtGui.QIcon("./swmmimages/12vert.png"))
        self.listWidget.item(12).setIcon(QtGui.QIcon("./swmmimages/13arch.png"))
        self.listWidget.item(13).setIcon(QtGui.QIcon("./swmmimages/14recttri.png"))
        self.listWidget.item(14).setIcon(QtGui.QIcon("./swmmimages/15rectround.png"))
        self.listWidget.item(15).setIcon(QtGui.QIcon("./swmmimages/16basket.png"))
        self.listWidget.item(16).setIcon(QtGui.QIcon("./swmmimages/17egg.png"))
        self.listWidget.item(17).setIcon(QtGui.QIcon("./swmmimages/18horse.png"))
        self.listWidget.item(18).setIcon(QtGui.QIcon("./swmmimages/19goth.png"))
        self.listWidget.item(19).setIcon(QtGui.QIcon("./swmmimages/20cat.png"))
        self.listWidget.item(20).setIcon(QtGui.QIcon("./swmmimages/21semi.png"))
        self.listWidget.item(21).setIcon(QtGui.QIcon("./swmmimages/22bask.png"))
        self.listWidget.item(22).setIcon(QtGui.QIcon("./swmmimages/23semi.png"))
        self.listWidget.item(23).setIcon(QtGui.QIcon("./swmmimages/24custom.png"))
        self.listWidget.item(24).setIcon(QtGui.QIcon("./swmmimages/25na.png"))

        self.listWidget_currentItemChanged()


    def cmdOK_Clicked(self):
        # will need to do some validating, see dxsect.pas
        cur = self.listWidget.currentItem()
        current_selection = ""
        if cur:
            current_selection = str(cur.text())

        section = self._main_form.project.find_section("XSECTIONS")
        link_list = section.value[0:]
        for value in link_list:
            if value.link == self.link_name:
                # this is the link we are editing
                value.barrels = self.sbxNumber.text()
                value.geometry1 = self.txt1.text()
                value.geometry2 = self.txt2.text()
                value.geometry3 = self.txt3.text()
                value.geometry4 = self.txt4.text()
                value.transect = ''
                value.curve = ''
                XType = ''
                if current_selection == 'Rectangular':
                    XType = 'RECT_OPEN'
                    value.geometry3 = int(self.cboCombo.currentIndex())
                elif current_selection == 'Trapezoidal':
                    XType = 'TRAPEZOIDAL'
                elif current_selection == 'Triangular':
                    XType = 'TRIANGULAR'
                elif current_selection == 'Parabolic':
                    XType = 'PARABOLIC'
                elif current_selection == 'Power':
                    XType = 'POWER'
                elif current_selection == 'Irregular':
                    XType = 'IRREGULAR'
                    value.transect = self.cboCombo.itemText(self.cboCombo.currentIndex())
                elif current_selection == 'Circular':
                    XType = 'CIRCULAR'
                elif current_selection == 'Force Main':
                    XType = 'FORCE_MAIN'
                elif current_selection == 'Filled Circular':
                    XType = 'FILLED_CIRCULAR'
                elif current_selection == 'Closed Rectangular':
                    XType = 'RECT_CLOSED'
                elif current_selection == 'Horizontal Elliptical':
                    XType = 'HORIZ_ELLIPSE'
                elif current_selection == 'Vertical Elliptical':
                    XType = 'VERT_ELLIPSE'
                elif current_selection == 'Arch':
                    XType = 'ARCH'
                elif current_selection == 'Rectangular Triangular':
                    XType = 'RECT_TRIANGULAR'
                elif current_selection == 'Rectangular Round':
                    XType = 'RECT_ROUND'
                elif current_selection == 'Modified Baskethandle':
                    XType = 'MODBASKETHANDLE'
                elif current_selection == 'Egg':
                    XType = 'EGG'
                elif current_selection == 'Horseshoe':
                    XType = 'HORSESHOE'
                elif current_selection == 'Gothic':
                    XType = 'GOTHIC'
                elif current_selection == 'Catenary':
                    XType = 'CATENARY'
                elif current_selection == 'Semi-Elliptical':
                    XType = 'SEMIELLIPTICAL'
                elif current_selection == 'Baskethandle':
                    XType = 'BASKETHANDLE'
                elif current_selection == 'Semi-Circular':
                    XType = 'SEMICIRCULAR'
                elif current_selection == 'Custom':
                    XType = 'CUSTOM'
                    value.curve = self.cboCombo.itemText(self.cboCombo.currentIndex())
                elif current_selection == 'Dummy':
                    XType = 'DUMMY'
                value.shape = core.swmm.hydraulics.link.CrossSectionShape[XType]
        self.close()


    def cmdCancel_Clicked(self):
        self.close()


    def btnDialog_Clicked(self):
        cur = self.listWidget.currentItem()
        current_selection = ""
        if cur:
            current_selection = str(cur.text())

        if current_selection == "Irregular":
            self._frmTransect = frmTransect(self._main_form)
            self._frmTransect.show()
        elif current_selection == 'Custom':
            self._frmCurveEditor = frmCurveEditor(self._main_form, 'SWMM Shape Curves', "SHAPE")
            self._frmCurveEditor.set_from(self._main_form.project, '')
            self._frmCurveEditor.show()


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
            # self.cboCombo.addItems() # need to set from available transects
            transect_section = self._main_form.project.find_section("TRANSECTS")
            transect_list = transect_section.value[0:]
            self.cboCombo.addItem("")
            for value in transect_list:
                if value.name:
                    self.cboCombo.addItem(value.name)
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
            dw_section = self._main_form.project.find_section("OPTIONS")
            if dw_section.force_main_equation == core.swmm.options.dynamic_wave.ForceMainEquation.H_W:
                self.lblFootnote.setText('*Hazen-Williams C-factor')
            if dw_section.force_main_equation == core.swmm.options.dynamic_wave.ForceMainEquation.D_W:
                if units == 1:
                    self.lblFootnote.setText('*Darcy-Weisbach roughness height (inches)')
                else:
                    self.lblFootnote.setText('*Darcy-Weisbach roughness height (mm)')
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
            self.cboCombo.clear()
            self.cboCombo.addItem('Custom')
            if units == 1:
                self.lblCombo.setText('Standard Sizes (inches)')
                for index in range(0,self.ellipse_major_axis_in.__len__()):
                    self.cboCombo.addItem(str(self.ellipse_minor_axis_in[index]) + ' x ' + str(self.ellipse_major_axis_in[index]))
            else:
                self.lblCombo.setText('Standard Sizes (mm)')
                for index in range(0,self.ellipse_major_axis_mm.__len__()):
                    self.cboCombo.addItem(str(self.ellipse_minor_axis_mm[index]) + ' x ' + str(self.ellipse_major_axis_mm[index]))
            self.lblBottom.setText('Closed horizontal elliptical pipe. Select a standard size or "Custom" to enter a custom height and width.')
        elif current_selection == 'Vertical Elliptical':
            XType = 'VERT_ELLIPSE'
            self.lblText2.setText('Maximum Width')
            self.lblText3.setText('Size Code')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            self.cboCombo.clear()
            self.cboCombo.addItem('Custom')
            if units == 1:
                self.lblCombo.setText('Standard Sizes (inches)')
                for index in range(0,self.ellipse_major_axis_in.__len__()):
                    self.cboCombo.addItem(str(self.ellipse_major_axis_in[index]) + ' x ' + str(self.ellipse_minor_axis_in[index]))
            else:
                self.lblCombo.setText('Standard Sizes (mm)')
                for index in range(0,self.ellipse_major_axis_mm.__len__()):
                    self.cboCombo.addItem(str(self.ellipse_major_axis_mm[index]) + ' x ' + str(self.ellipse_minor_axis_mm[index]))
            self.lblBottom.setText('Closed vertical elliptical pipe. Select a standard size or "Custom" to enter a custom height and width.')
        elif current_selection == 'Arch':
            XType = 'ARCH'
            self.lblText2.setText('Maximum Width')
            self.lblText3.setText('Size Code')
            self.lblText4.setVisible(False)
            self.txt4.setVisible(False)
            self.lblCombo.setVisible(True)
            self.cboCombo.setVisible(True)
            self.cboCombo.clear()
            self.cboCombo.addItem('Custom')
            if units == 1:
                self.lblCombo.setText('Standard Sizes (inches)')
                for index in range(0,self.arch_type.__len__()):
                    self.cboCombo.addItem(str(self.arch_type[index]) + ' ' + str(self.arch_height_in[index] + ' x '
                                            + str(self.arch_width_in[index])))
            else:
                self.lblCombo.setText('Standard Sizes (mm)')
                for index in range(0,self.ellipse_major_axis_mm.__len__()):
                    width_mm = str(float(self.arch_width_in[index]) * 25.4)
                    height_mm = str(float(self.arch_height_in[index]) * 25.4)
                    self.cboCombo.addItem(str(self.arch_type[index]) + ' ' + height_mm + ' x ' + width_mm)
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
            curves_section = self._main_form.project.curves
            self.cboCombo.addItem("")
            for curve in curves_section.value:
                if curve.name and curve.curve_type == CurveType.SHAPE:
                    self.cboCombo.addItem(curve.name)
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

    def cboCombo_currentIndexChanged(self):
        cur = self.listWidget.currentItem()
        current_selection = ""
        if cur:
            current_selection = str(cur.text())

        units = 1
        if units == 1:
            factor = 12
        else:
            factor = 39.3701

        if current_selection == 'Horizontal Elliptical':
            selected_index = self.cboCombo.currentIndex()
            if self.ellipse_minor_axis_in:
                self.txt1.setText(str(float(self.ellipse_minor_axis_in[selected_index-1])/factor))
                self.txt2.setText(str(float(self.ellipse_major_axis_in[selected_index-1])/factor))
                self.txt3.setText(str(selected_index))
        elif current_selection == 'Vertical Elliptical':
            selected_index = self.cboCombo.currentIndex()
            if self.ellipse_minor_axis_in:
                self.txt1.setText(str(float(self.ellipse_major_axis_in[selected_index-1])/factor))
                self.txt2.setText(str(float(self.ellipse_minor_axis_in[selected_index-1])/factor))
                self.txt3.setText(str(selected_index))
        elif current_selection == 'Arch':
            selected_index = self.cboCombo.currentIndex()
            if self.arch_height_in:
                self.txt1.setText(str(float(self.arch_height_in[selected_index-1])/factor))
                self.txt2.setText(str(float(self.arch_width_in[selected_index-1])/factor))
                self.txt3.setText(str(selected_index))
