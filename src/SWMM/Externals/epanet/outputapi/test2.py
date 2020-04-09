"""example: call thougt functionalwrapper  module

"""
import functionalwrapper  as ENob

filename="Net1.bin" 

try:
   netout= ENob.open(filename)
except  ENob.EnOutErr as e:
  print e
  exit()

print "nodes:",   ENob.getnumnodes(netout)
print "tanks:",   ENob.getnumtanks(netout)
print "links:",   ENob.getnumlinks(netout)
print "pumps:",   ENob.getnumpumps(netout)
print "valves:",  ENob.getnumvalves(netout)

numperiods= ENob.getnumperiods(netout)
index= 10
nodeID= ENob.getnodeid(netout, index)
print "\n\nHead at node index={0}, ID={1} for {2} periods".format( index, nodeID, numperiods)

for i in range(0, numperiods):
    print ENob.getnodehead(netout, timeidx=i, nodeidx=index),
print "\n\n"

ENob.close(netout)

# try:
#   netout= ENob.open('nonexists')
# except  ENob.EnOutErr as e:
#   print "voluntary error -->{0}".format(e)