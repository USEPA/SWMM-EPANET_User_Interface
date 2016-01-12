import plugins.Summary.summarizeConduits
import plugins.Summary.summarizeNodes
import plugins.Summary.summarizePressureHeads
import plugins.Summary.summarizeSubbasins
import pymsgbox

plugin_name = "Summary"
plugin_create_menu = True
__all__ = {'Conduits':1, 'Nodes':2, 'PressureHeads':3, 'Subbasins':4}


def run(*args):
    ltopTitle = 'Plugin:Summary'
    if args.__len__() > 0:
        lchoice = args[0]
    else:
        lchoice = 99
    if lchoice == 1:
        pymsgbox.alert(plugins.Summary.summarizeConduits.run(), ltopTitle)
    elif lchoice == 2:
        pymsgbox.alert(plugins.Summary.summarizeNodes.run(), ltopTitle)
    elif lchoice == 3:
        pymsgbox.alert(plugins.Summary.summarizePressureHeads.run(), ltopTitle)
    elif lchoice == 4:
        pymsgbox.alert(plugins.Summary.summarizeSubbasins.run(), ltopTitle)
    else:
        pymsgbox.alert("Top level summary is done.", ltopTitle)
