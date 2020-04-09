"""example: call thougt modified ENOutputWrapper  module

"""
from Externals.epanet.outputapi import ENOutputWrapper as eow

binfile = 'Net1.bin'

print("Testing Wrapper...")
print("Test {0}".format(binfile) )
print("\n-->Reading Binary File")
test_outobject = eow.OutputObject(binfile)
print("...Opened Bin File")

print("\n-->get_NodeSeries")
LENTest = -1
demands = test_outobject.get_NodeSeries(0,eow.ENR_demand, 0, LENTest)
head = test_outobject.get_NodeSeries(0,eow.ENR_head, 0, LENTest)
pressure = test_outobject.get_NodeSeries(0,eow.ENR_pressure, 0, LENTest)
quality = test_outobject.get_NodeSeries(0,eow.ENR_quality, 0, LENTest)
print('\t'.join(["TimeIndx","demand","head","pressure","quality"]))
for ind in range(test_outobject.num_periods):
    print ind, demands[ind], head[ind], pressure[ind], quality[ind]

print("\n-->get_LinkSeries")
flow = test_outobject.get_LinkSeries(0,eow.ENR_flow)
velocity =test_outobject.get_LinkSeries(0,eow.ENR_velocity)
headloss =test_outobject.get_LinkSeries(0,eow.ENR_headloss)
avgQuality=test_outobject.get_LinkSeries(0,eow.ENR_avgQuality)
status=test_outobject.get_LinkSeries(0,eow.ENR_status)
setting=test_outobject.get_LinkSeries(0,eow.ENR_setting)
rxRate=test_outobject.get_LinkSeries(0,eow.ENR_rxRate)
frctnFctr =test_outobject.get_LinkSeries(0,eow.ENR_frctnFctr)
print('\t'.join(["TimeInd","flow","velocity","headloss","avgQuality",
                 "status","setting","rxRate","frctnFctr"]))
for ind in range(test_outobject.num_periods ):
    print ind, flow[ind], velocity[ind],headloss[ind],avgQuality[ind],status[ind],setting[ind],rxRate[ind],frctnFctr[ind]

print("\n--> like get_LinkSeries but with get_LinkValue")
LinkInd= 0
print('\t'.join(["TimeInd","flow","velocity","headloss","avgQuality",
                 "status","setting","rxRate","frctnFctr"]))
for TimeInd in range(test_outobject.num_periods):
   print TimeInd,
   for LinkAttr in eow.ENR_LinkAttributes:
       print test_outobject.get_LinkValue(LinkInd, TimeInd,  LinkAttr),
   print




print("\n-->get_NodeAttribute")
demand_1 = test_outobject.get_NodeAttribute(eow.ENR_demand,0)
head_1 = test_outobject.get_NodeAttribute(eow.ENR_head,0)
pressure_1 = test_outobject.get_NodeAttribute(eow.ENR_pressure,0)
quality_1 = test_outobject.get_NodeAttribute(eow.ENR_quality,0)
print('\t'.join(["ID","demand","head","pressure","quality"]))
for ind in range(test_outobject.nodeCount):
    print test_outobject.get_NodeID(ind), demand_1[ind], head_1[ind], pressure_1[ind], quality_1[ind]
    

print("\n--> like get_NodeAttribute but with get_NodeValue")
print('\t'.join(["ID","demand","head","pressure","quality"]))
TimeInd= 0
for NodeInd in range(test_outobject.nodeCount):
   print test_outobject.get_NodeID(NodeInd),
   for NodeAttr in eow.ENR_NodeAttributes:
       print test_outobject.get_NodeValue(NodeInd, TimeInd,  NodeAttr),
   print


print("\n-->get_LinkAttribute")
flow1 = test_outobject.get_LinkAttribute(eow.ENR_flow,0)
velocity1 =test_outobject.get_LinkAttribute(eow.ENR_velocity,0)
headloss1 =test_outobject.get_LinkAttribute(eow.ENR_headloss,0)
avgQuality1=test_outobject.get_LinkAttribute(eow.ENR_avgQuality,0)
status1=test_outobject.get_LinkAttribute(eow.ENR_status,0)
setting1=test_outobject.get_LinkAttribute(eow.ENR_setting,0)
rxRate1=test_outobject.get_LinkAttribute(eow.ENR_rxRate,0)
frctnFctr1 =test_outobject.get_LinkAttribute(eow.ENR_frctnFctr,0)
print('\t'.join(["ind","flow","velocity","headloss","avgQuality",\
                 "status","setting","rxRate","frctnFctr"]))
for ind in range(test_outobject.linkCount):
    print test_outobject.get_LinkID(ind), flow1[ind], velocity1[ind],headloss1[ind],avgQuality1[ind],status1[ind],setting1[ind],rxRate1[ind],frctnFctr1[ind]



print("\n-->Object Counts")
print("Nodes")
print(test_outobject.nodeCount)
print("Nodes")
print(test_outobject.nodeCount)    
print("Tanks")
print(test_outobject.tankCount)
print("Links")
print(test_outobject.linkCount)
print("Pumps")
print(test_outobject.pumpCount)
print("Valves")
print(test_outobject.valveCount)     


print("\n-->get_NodeResult")
print(test_outobject.get_NodeResult(96,24))

print("\n-->get_LinkResult")
print(test_outobject.get_LinkResult(0,0))    

print("\n-->get_Units")
print("...flow unit code")
print(test_outobject.flowUnits)
print("...pressure unit code")
print(test_outobject.pressUnits)

print("\n-->Closing Binary File")
test_outobject.CloseOutputFile()
print("...Closed Binary File")
