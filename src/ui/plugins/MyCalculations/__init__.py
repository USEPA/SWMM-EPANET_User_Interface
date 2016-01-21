import pymsgbox
plugin_name = 'MyCalculations'
plugin_create_menu = False
__all__ = {}
def run():
    ltopTitle = 'Plugin:MyCalculations'
    pymsgbox.alert("Custom user calculation is done.", ltopTitle)
