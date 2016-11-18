import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmProfilePlotDesigner import Ui_frmProfilePlot
from ui.help import HelpHandler
import core.swmm.hydraulics.node


class frmProfilePlot(QtGui.QMainWindow, Ui_frmProfilePlot):
    MAGIC = "SWMM_PROFILE_GRAPH_SPEC:\n"

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/profileplotoptionsdialog.htm"
        self._main_form = main_form
        self.setupUi(self)
        self.cmdFind.setEnabled(False)  # TODO: Enable when functionality is ready
        self.cmdSave.setText("Copy")
        self.cmdUse.setText("Paste")
        QtCore.QObject.connect(self.cmdSave, QtCore.SIGNAL("clicked()"), self.cmdSave_Clicked)
        QtCore.QObject.connect(self.cmdUse, QtCore.SIGNAL("clicked()"), self.cmdUse_Clicked)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.cmdFind, QtCore.SIGNAL("clicked()"), self.cmdFind_Clicked)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        self.cboEnd.clear()
        if project and self.output:
            for node_name in self.output.nodes:
                self.cboStart.addItem(node_name)
                self.cboEnd.addItem(node_name)
                self.cmdFind.setEnabled(True)
            #for link_name in self.output.links:
            #    self.lstData.addItem(link_name)

    def get_text(self):
        return self.MAGIC + '\n'.join([str(self.lstData.item(i).text()) for i in range(self.lstData.count())])

    def set_from_text(self, text):
        if text.startswith(self.MAGIC):
            self.lstData.clear()
            for line in text[len(self.MAGIC):].split('\n'):
                self.lstData.addItem(line)

    def cmdFind_Clicked(self):
        self.lstData.clear()
        start_node = str(self.cboStart.currentText())
        end_node = str(self.cboEnd.currentText())

        current_node = start_node
        counter = 0
        while current_node <> end_node and counter < 1000:
            counter += 1
            for link_group in self.project.links_groups():
                if link_group and link_group.value:
                    for link in link_group.value:
                        if link.inlet_node == current_node and current_node <> end_node:
                            self.lstData.addItem(link.name)
                            current_node = link.outlet_node

    def cmdSave_Clicked(self):
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.get_text(), mode=cb.Clipboard)

    def cmdUse_Clicked(self):
        try:
            self.set_from_text(QtGui.QApplication.clipboard().text())
        except Exception as ex:
            print(str(ex))
            self.lstData.clear()

    def cmdCancel_Clicked(self):
        self.close()

    def cmdOK_Clicked(self):
        # Profile plot based on 'Basic HGL 2-D Video Profile Plot Script by Bryant E. McDonnell'

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import numpy as np
        from scipy.interpolate import interp1d

        # Show Plot 1 = SHOW; 2 = Save Video Plot; 3 = Export HTML
        fig_output = 1

        # Pass Ordered Links
        self.lstData.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.lstData.selectAll()
        LKsToPlot = []
        for selected_item in self.lstData.selectedItems():
            LKsToPlot.append(str(selected_item.text()))

        # #pass Appendix (If desired, else set to [])
        LKsToPlotAppendix = []

        appendpltdir = -1 # Appendix direction: can be -1 for left and 1 for right

        mhrad = 7 # ft (Assumed manhole radius for plot purposes.  Value is adjustable)

        # Input file Hydraulic Data
        # Conduit ID,  US Node, DS,    Len, Diameter, US offset, DS offset
        start_node = ''
        end_node = ''
        LKsToPlotData = {}
        for link_name in LKsToPlot:
            try:
                link = self.project.find_link(link_name)
                nodes = (link.inlet_node, link.outlet_node)
                diameter = 0
                for cross_section in self.project.xsections.value:
                    if cross_section.link == link_name:
                        diameter = cross_section.geometry1
                length = 10
                if isinstance(link,core.swmm.hydraulics.link.Conduit):
                    length = float(link.length) - 2*mhrad
                inlet_offset = 10
                if isinstance(link,core.swmm.hydraulics.link.Conduit):
                    inlet_offset = link.inlet_offset
                outlet_offset = 10
                if isinstance(link,core.swmm.hydraulics.link.Conduit):
                    outlet_offset = link.outlet_offset
                LKsToPlotData[link_name] = [nodes, length, diameter, inlet_offset, outlet_offset]
                # this is also a convenient place to record the start and end nodes for use in the title
                if len(start_node) == 0:
                    start_node = link.inlet_node
                end_node = link.outlet_node
            except:
                pass  # probably did not find link in this group, move on to the next group

        NodeInverts = {}
        NodeDepths = {}
        for node_group in self.project.nodes_groups():
            if node_group and node_group.value:
                for node in node_group.value:
                    elevation = 0
                    depth = 0
                    if node.elevation:
                        elevation = node.elevation
                    if isinstance(node,core.swmm.hydraulics.node.Junction):
                        depth = node.max_depth
                    NodeInverts[node.name] = elevation
                    NodeDepths[node.name] = depth

        global ApLnks
        ApLnks = len(LKsToPlotAppendix)

        # plot the Infrastructure data
        MHList,LinkSpanList,InvertEl = [],[],[]
        for ind,ID in enumerate(LKsToPlot):
            if ind == 0:
                MHList.append(LKsToPlotData[ID][0][0])
                InvertEl.append(NodeInverts[LKsToPlotData[ID][0][0]])

            MHList.append(LKsToPlotData[ID][0][1])
            InvertEl.append(NodeInverts[LKsToPlotData[ID][0][1]])
            LinkSpanList.append(LKsToPlotData[ID][1])


        if len(LKsToPlotAppendix)>0:
            MHListAppendix,LinkSpanListAppendix,InvertElAppendix = [],[],[]
            for ind,ID in enumerate(LKsToPlotAppendix):
                if ind == 0:
                    MHListAppendix.append(LKsToPlotData[ID][0][0])
                    InvertElAppendix.append(NodeInverts[LKsToPlotData[ID][0][0]])

                MHListAppendix.append(LKsToPlotData[ID][0][1])
                InvertElAppendix.append(NodeInverts[LKsToPlotData[ID][0][1]])
                LinkSpanListAppendix.append(LKsToPlotData[ID][1])


        pltxspans=np.zeros(2*len(MHList))
        MHDepthspans=np.zeros(2*len(MHList))
        Groundspans=np.zeros(2*len(MHList))
        INVELspan =np.zeros(2*len(MHList))
        mhind = 0
        lnkind = 0
        for ind,val in enumerate(pltxspans):
            if ind == 0:
                pltxspans[0] = 0.0
                MHDepthspans[0] = float( NodeDepths[MHList[mhind]] )
                INVELspan[0] = float( NodeInverts[MHList[mhind]] )
                Groundspans[0] = INVELspan[0]+ MHDepthspans[0]
            elif (ind + 1) % 2 == 0:
                pltxspans[ind] = pltxspans[ind-1]+2*mhrad
                INVELspan[ind] = float( NodeInverts[MHList[mhind]] )
                try: #make this more generic later
                    MHDepthspans[ind] = float( NodeDepths[MHList[mhind]] )
                except:
                    MHDepthspans[ind] = 0.0
                Groundspans[ind] = float( NodeInverts[MHList[mhind]] )+float( NodeDepths[MHList[mhind]] )
            else:
                mhind+=1
                pltxspans[ind] = pltxspans[ind-1]+float(LinkSpanList[lnkind])
                try: #make this more generic later
                    MHDepthspans[ind] = float( NodeDepths[MHList[mhind]] )
                except:
                    MHDepthspans[ind] = 0.0
                Groundspans[ind] = float( NodeInverts[MHList[mhind]] )+float( NodeDepths[MHList[mhind]] )
                INVELspan[ind] = float( NodeInverts[MHList[mhind]] )
                lnkind+=1

        if len(LKsToPlotAppendix)>0:
            # Find where the MHs Match up if direction
            pltxspansAppendix=np.zeros(2*len(MHListAppendix))
            GroundspansAppendix=np.zeros(2*len(MHListAppendix))
            mhindex = MHList.index(MHListAppendix[0])
            MHDepthspansAppendix=np.zeros(2*len(MHListAppendix))
            INVELspanAppendix =np.zeros(2*len(MHListAppendix))
            mhindAppendix = 0
            lnkindAppendix = 0

            if appendpltdir == 1:
                pltxspansAppendix[0] = pltxspans[mhindex*2]
                GroundspansAppendix[0] = float( NodeInverts[MHListAppendix[mhindAppendix]] )+float( NodeDepths[MHListAppendix[mhindAppendix]] )

            elif appendpltdir == -1:
                pltxspansAppendix[0] = pltxspans[mhindex*2+1]
                GroundspansAppendix[0] = float( NodeInverts[MHListAppendix[mhindAppendix]] )+float( NodeDepths[MHListAppendix[mhindAppendix]] )

            for ind,val in enumerate(pltxspansAppendix):
                if ind == 0:
                    MHDepthspansAppendix[0] = float( NodeDepths[MHListAppendix[mhindAppendix]] )
                    INVELspanAppendix[0] = float( NodeInverts[MHListAppendix[mhindAppendix]] )

                elif (ind + 1) % 2 == 0:
                    pltxspansAppendix[ind] = pltxspansAppendix[ind-1]+appendpltdir*2*mhrad
                    INVELspanAppendix[ind] = float( NodeInverts[MHListAppendix[mhindAppendix]] )
                    try: #make this more generic later
                        MHDepthspansAppendix[ind] = float( NodeDepths[MHListAppendix[mhindAppendix]] )
                    except:
                        MHDepthspansAppendix[ind] = 0.0
                    GroundspansAppendix[ind] = float( NodeDepths[MHListAppendix[mhindAppendix]] )+float( NodeInverts[MHListAppendix[mhindAppendix]] )
                else:
                    mhindAppendix += 1
                    pltxspansAppendix[ind] = pltxspansAppendix[ind-1]+appendpltdir*float(LinkSpanListAppendix[lnkindAppendix])
                    try: # make this more generic later
                        MHDepthspansAppendix[ind] = float( NodeDepths[MHListAppendix[mhindAppendix]] )
                    except:
                        MHDepthspansAppendix[ind] = 0.0
                    GroundspansAppendix[ind] = float( NodeDepths[MHListAppendix[mhindAppendix]] )+float( NodeInverts[MHListAppendix[mhindAppendix]] )
                    INVELspanAppendix[ind] = float( NodeInverts[MHListAppendix[mhindAppendix]] )
                    lnkindAppendix += 1

        # Read Model output Data
        OutputObject = self.output
        NPeriods = OutputObject.num_periods
        # print MHList, LinkSpanList, InvertEl, pltxspans,MHDepthspans,INVELspan
        RESULTMATRIX = np.zeros((len(MHList),NPeriods))
        for ind,ID in enumerate(MHList):
            node = OutputObject.nodes[ID]
            RESULTMATRIX[ind,:]=node.get_series(OutputObject, node.attribute_head)

        if len(LKsToPlotAppendix)>0:
            RESULTMATRIXAppendix = np.zeros((len(MHListAppendix),NPeriods ))
            for ind,ID in enumerate(MHListAppendix):
                node = OutputObject.nodes[ID]
                RESULTMATRIXAppendix[ind,:]=node.get_series(OutputObject, node.attribute_head)


        def data_gen():
            # Function is called by the matplotlib animation tools to update the HGL and Peak HGL
            global ApLnks
            t = data_gen.t
            cnt = 0
            # print 'data_gen' + str(ApLnks)
            while cnt < NPeriods -1:
                cnt += 1
                t += 1
                if ApLnks == 0:
                    yield t, RESULTMATRIX[:,cnt]
                elif ApLnks > 0:
                    yield t, RESULTMATRIX[:,cnt],RESULTMATRIXAppendix[:,cnt]
        data_gen.t = 0




        fig, ax = plt.subplots()
        ax.grid()
        line, = ax.plot([], [], lw=2, c='b')
        liney2, = ax.plot([], [], lw=2, c='b')
        # peak HGL
        line2, = ax.plot([], [], lw=1, c='r')
        line2y2, = ax.plot([], [], lw=1, c='r')
        global HGL_max
        HGL_max = np.zeros(len(pltxspans))

        if len(LKsToPlotAppendix)>0:
            global HGL_maxy2
            HGL_maxy2 = np.zeros(len(pltxspansAppendix))
        else:
            pltxspansAppendix = [100000000]

        tex = ax.text(min(min(pltxspans),min(pltxspansAppendix))+20,min(INVELspan), '')
        plt.xlabel("Distance (ft)")
        plt.ylabel("Elevation (ft)")
        fig.canvas.set_window_title('Profile - Node ' + start_node + ' - ' + end_node)

        # ax.legend([line, line2],['HGL f(t)','PEAK HGL'], loc = 4)
        ax.legend([line],['HGL f(t)'], loc = 4)


        # MH PLOTS boxes
        for ind,val in enumerate(MHList):
            front,back = ind*2,ind*2+1
            plt.plot([pltxspans[front],pltxspans[back]],\
                     [INVELspan[front],INVELspan[back]],'-k')
            plt.plot([pltxspans[front],pltxspans[back]],\
                     [INVELspan[front]+MHDepthspans[front],INVELspan[back]+MHDepthspans[back]],'-k')
            plt.plot([pltxspans[front],pltxspans[front]],\
                     [INVELspan[front],INVELspan[front]+MHDepthspans[front]],'-k')
            plt.plot([pltxspans[back],pltxspans[back]],\
                     [INVELspan[back],INVELspan[back]+MHDepthspans[back]],'-k')
            # MH Naming Text Plotting
            if ind%2 == 0:
                texmh = plt.text(pltxspans[front],INVELspan[front]+MHDepthspans[front],\
                         '   '+val,horizontalalignment = 'left',verticalalignment='bottom',rotation = 'vertical')
                texmh.set_fontsize(11)

        # LINK PLOTS boxes
        lnkinvelud = []
        for ind,ID in enumerate(LKsToPlot):
            up,down = ind*2+1,ind*2+2
            plt.plot([pltxspans[up],pltxspans[down]],\
                     [INVELspan[up]+float(LKsToPlotData[ID][3]),\
                      INVELspan[down]+float(LKsToPlotData[ID][4])],'-k')
            lnkinvelud.append(INVELspan[up]+float(LKsToPlotData[ID][3]))
            lnkinvelud.append(INVELspan[down]+float(LKsToPlotData[ID][4]))
            plt.plot([pltxspans[up],pltxspans[down]],\
                     [INVELspan[up]+float(LKsToPlotData[ID][3])+float(LKsToPlotData[ID][2]),\
                      INVELspan[down]+float(LKsToPlotData[ID][4])+float(LKsToPlotData[ID][2])],'-k')


        # GROUND LEVEL PLOT
        func = interp1d(pltxspans,Groundspans,kind='cubic')
        xinterp = np.linspace(min(pltxspans),max(pltxspans),300)
        plt.plot(xinterp,func(xinterp), ':k')

        if len(LKsToPlotAppendix)>0:
            for ind,val in enumerate(MHListAppendix):
                front,back = ind*2,ind*2+1
                plt.plot([pltxspansAppendix[front],pltxspansAppendix[back]],\
                         [INVELspanAppendix[front],INVELspanAppendix[back]],'-k')
                plt.plot([pltxspansAppendix[front],pltxspansAppendix[back]],\
                         [INVELspanAppendix[front]+MHDepthspansAppendix[front],INVELspanAppendix[back]+MHDepthspansAppendix[back]],'-k')
                plt.plot([pltxspansAppendix[front],pltxspansAppendix[front]],\
                         [INVELspanAppendix[front],INVELspanAppendix[front]+MHDepthspansAppendix[front]],'-k')
                plt.plot([pltxspansAppendix[back],pltxspansAppendix[back]],\
                         [INVELspanAppendix[back],INVELspanAppendix[back]+MHDepthspansAppendix[back]],'-k')

            # LINK PLOTS
            lnkinveludAppendix = []
            for ind,ID in enumerate(LKsToPlotAppendix):
                up,down = ind*2+1,ind*2+2
                plt.plot([pltxspansAppendix[up],pltxspansAppendix[down]],\
                         [INVELspanAppendix[up]+float(LKsToPlotData[ID][3]),\
                          INVELspanAppendix[down]+float(LKsToPlotData[ID][4])],'-k')
                lnkinveludAppendix.append(INVELspanAppendix[up]+float(LKsToPlotData[ID][3]))
                lnkinveludAppendix.append(INVELspanAppendix[down]+float(LKsToPlotData[ID][4]))
                plt.plot([pltxspansAppendix[up],pltxspansAppendix[down]],\
                         [INVELspanAppendix[up]+float(LKsToPlotData[ID][3])+float(LKsToPlotData[ID][2]),\
                          INVELspanAppendix[down]+float(LKsToPlotData[ID][4])+float(LKsToPlotData[ID][2])],'-k')
            # GROUND LEVEL PLOT
            sortx = pltxspansAppendix.argsort()
            func1 = interp1d(pltxspansAppendix[sortx],GroundspansAppendix[sortx],kind='linear')
            xinterpAppendix = np.linspace(min(pltxspansAppendix),max(pltxspansAppendix),300)
            plt.plot(xinterpAppendix,func1(xinterpAppendix), ':k')

        def run(data):
            global ApLnks
            if ApLnks == 0:
                t,y = data
                HGL_data = np.zeros(len(pltxspans))
                for ind,val in enumerate(y):
                    if ind == 0:
                        HGL_data[ind*2] = val
                    else:
                        if val < lnkinvelud[ind*2-1]:
                            HGL_data[ind*2] =  lnkinvelud[ind*2-1]
                        else:
                            HGL_data[ind*2] = val
                    if ind == len(y)-1:
                        HGL_data[ind*2+1] = val
                    else:
                        if val < lnkinvelud[ind*2]:
                            HGL_data[ind*2+1] =  lnkinvelud[ind*2]
                        else:
                            HGL_data[ind*2+1] = val
                line.set_data(pltxspans,HGL_data)

            elif ApLnks >0:
                t,y,yapp = data
                HGL_data = np.zeros(len(pltxspans))
                for ind,val in enumerate(y):
                    if ind == 0:
                        HGL_data[ind*2] = val
                    else:
                        if val < lnkinvelud[ind*2-1]:
                            HGL_data[ind*2] =  lnkinvelud[ind*2-1]
                        else:
                            HGL_data[ind*2] = val
                    if ind == len(y)-1:
                        HGL_data[ind*2+1] = val
                    else:
                        if val < lnkinvelud[ind*2]:
                            HGL_data[ind*2+1] =  lnkinvelud[ind*2]
                        else:
                            HGL_data[ind*2+1] = val

                HGL_dataAppendix = np.zeros(len(pltxspansAppendix))
                for ind,val in enumerate(yapp):
                    #print ind
                    if ind == 0:
                        HGL_dataAppendix[ind*2] = val
                    else:
                        if val < lnkinveludAppendix[ind*2-1]:
                            HGL_dataAppendix[ind*2] =  lnkinveludAppendix[ind*2-1]
                        else:
                            HGL_dataAppendix[ind*2] = val

                    if ind == len(yapp)-1:
                        HGL_dataAppendix[ind*2+1] = val
                    else:
                        if val < lnkinveludAppendix[ind*2]:
                            HGL_dataAppendix[ind*2+1] =  lnkinveludAppendix[ind*2]
                        else:
                            HGL_dataAppendix[ind*2+1] = val
                line.set_data(pltxspans,HGL_data)
                liney2.set_data(pltxspansAppendix,HGL_dataAppendix)

            # PEAK HGL
            # global HGL_max
            # HGL_max = np.vstack((HGL_max,HGL_data))
            # line2.set_data(pltxspans,HGL_max.max(0))
            #  if ApLnks > 0:
            #    global HGL_maxy2
            #    HGL_maxy2 = np.vstack((HGL_maxy2,HGL_dataAppendix))
            #    line2y2.set_data(pltxspansAppendix,HGL_maxy2.max(0))

            # Interval Text Note
            tex.set_text("Interval " + str(t))
            return line,tex


        ani = animation.FuncAnimation(fig, run, data_gen, save_count = NPeriods ,blit=False)

        if fig_output == 1:
            plt.show()

        if fig_output == 2:
            ani.save('basic_animation.mp4',fps=30, bitrate=2000)

        # if fig_output == 3:
        #     from JSAnimation import HTMLWriter
        #     ani.save('Basic.html', writer=HTMLWriter(embed_frames=False),extra_args=['figsize',[15,6],'dpi',250])

        self.close()

