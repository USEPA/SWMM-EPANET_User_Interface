'''
Basic HGL 2-D Video Profile Plot Scipt


Author: Bryant E. McDonnell
Date:    01/10/2010
Updated: 07/25/2016



'''

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.interpolate import interp1d

# sys.path.append('C:/devNotMW/GitHub/SWMM-EPANET_User_Interface_dev_ui/src/Externals/swmm/outputapi')
from Externals.swmm.outputapi.SMOutputSWIG import *


#Show Plot 1 = SHOW; 2 = Save Video Plot; 3 = Export HTML
fig_output = 1

#Pass Ordered Links 
LKsToPlot = ['9-8','8-7','7-6','6-5','10-5',\
             '11-10','12-11','13-12','14-13','15-14']

#pass Appendix (If desired, else set to [])
LKsToPlotAppendix =  ['5-4','4-3','3-2','2-1','1-0']

appendpltdir = -1 # Appendix direction: can be -1 for left and 1 for right

mhrad = 7#ft (Assumed manhole radius for plot purposes.  Value is adjustable)

'''
Input file Hydraulic Data

'''
        #Conduit ID,  US Node, DS,    Len, Diameter, US offset, DS offset          
LKsToPlotData = {'9-8':  [['9','8'],  384, 2.5, 0, 0],\
                 '8-7':  [['8','7'],  410, 2.5, 0, 0], \
                 '7-6':  [['7','6'],  377, 2.5, 0, 0], \
                 '6-5':  [['6','5'],  492, 2.5, 0, 0], \
                 '10-5': [['10','5'], 42,  1.5, 0, 0],\
                 '11-10':[['11','10'],35,  2,   0, 0], \
                 '12-11':[['12','11'],129, 2,   0, 0], \
                 '13-12':[['13','12'],167, 2,   0, 0], \
                 '14-13':[['14','13'],454, 2,   0, 0], \
                 '15-14':[['15','14'],396, 2,   0, 0],\
                 '5-4':  [['5','4'],  202, 2.5, 0, 0],\
                 '4-3':  [['4','3'],  400, 2.5, 0, 0],\
                 '3-2':  [['3','2'],  195, 2.5, 0, 0],\
                 '2-1':  [['2','1'],  204, 3,   0, 0],\
                 '1-0':  [['1','0'],  257, 3,   0, 0]}

NodeInverts = {'1':0,'10':30.54,'11':31.64,'12':32.53,'13':33.56,'14':36.36,\
               '15':42.55,'16':47.41,'2':0.96,'3':14.58,'4':18.52,'5':20.06,'6':23.11,\
               '7':25.59,'8':27.94,'9':30.22, '0':0}

NodeDepths = {'1':15,'10':6,'11':6,'12':7,'13':7,'14':12,'15':12,'16':6,\
                '2':17,'3':10,'4':24,'5':13,'6':11,'7':11,'8':20,'9':13, '0':5}


'''
This quick version of the tool does quite a bit of plumbing...


'''




global ApLnks
ApLnks = len(LKsToPlotAppendix)





#plot the Infrastructure data
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
            mhindAppendix+=1
            pltxspansAppendix[ind] = pltxspansAppendix[ind-1]+appendpltdir*float(LinkSpanListAppendix[lnkindAppendix])
            try: #make this more generic later
                MHDepthspansAppendix[ind] = float( NodeDepths[MHListAppendix[mhindAppendix]] )
            except:
                MHDepthspansAppendix[ind] = 0.0
            GroundspansAppendix[ind] = float( NodeDepths[MHListAppendix[mhindAppendix]] )+float( NodeInverts[MHListAppendix[mhindAppendix]] )       
            INVELspanAppendix[ind] = float( NodeInverts[MHListAppendix[mhindAppendix]] )
            lnkindAppendix+=1

# Read Model output Data
# OutputObject = SwmmOutputObjects(dllLoc = 'C:/PROJECTCODE/SWMMOutputAPI/data/outputAPI_winx86.dll') #<- 07/25/2016 use LargeFS-32 branch of https://github.com/bemcdonnell/SWMMOutputAPI
OutputObject = SwmmOutputObject('/devNotMW/GitHub/SWMMProfilePlotTool/TestModel/SanitizedModel.out')
NPeriods = OutputObject.num_periods
#print MHList, LinkSpanList, InvertEl, pltxspans,MHDepthspans,INVELspan
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
    '''
    Function is called by the matplotlib animation tools to update the HGL and Peak HGL
    '''
    global ApLnks
    t = data_gen.t
    cnt = 0
    #print 'data_gen' + str(ApLnks)
    while cnt < NPeriods -1:
        cnt+=1
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
#peak HGL
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

ax.legend([line, line2],['HGL f(t)','PEAK HGL'], loc = 4)


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
    global HGL_max
    HGL_max = np.vstack((HGL_max,HGL_data))
    line2.set_data(pltxspans,HGL_max.max(0))
    if ApLnks > 0:
        global HGL_maxy2
        HGL_maxy2 = np.vstack((HGL_maxy2,HGL_dataAppendix))
        line2y2.set_data(pltxspansAppendix,HGL_maxy2.max(0))
        
    # Interval Text Note
    tex.set_text("Interval " + str(t))
    return line,tex


ani = animation.FuncAnimation(fig, run, data_gen, save_count = NPeriods ,blit=True)

if fig_output == 1:
    plt.show()
    
if fig_output == 2:
    ani.save('basic_animation.mp4',fps=30, bitrate=2000)

# if fig_output == 3:
#     from JSAnimation import HTMLWriter
#     ani.save('Basic.html', writer=HTMLWriter(embed_frames=False),extra_args=['figsize',[15,6],'dpi',250])









