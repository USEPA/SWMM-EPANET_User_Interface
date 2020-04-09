# SWMM and EPANET User Interface Source Code

Each form may have three files: 
- <form name>Designer.ui: file saved by Qt Designer specifying the layout of controls
- <form name>Designer.py: Python code automatically generated from the Designer.ui file
- <form name>.py: Python code handling the form's behavior and interaction with the main program

Folders:

* [EPANET](EPANET), [SWMM](SWMM): model-specific forms and behavior

Source Code:

* [convenience](convenience.py): Methods for interacting with Qt controls
* [editor](editor.py): Script editor form
* [embed_ipython_new](embed_ipython_new.py): Not in use, was for using iPython script editor
* [frmGenericListOutput](frmGenericListOutput.py): Display for a grid of data
* [frmGenericPropertyEditor](frmGenericPropertyEditor.py): Display and allow editing of properties
* [frmMain](frmMain.py): Main form base class for frmMainEPANET and frmMainSWMM
* [frmMapAddVector](frmMapAddVector.py): Form for adding a vector layer from a GIS file (not in use)
* [frmMapDimensions](frmMapDimensions.py): Form for editing map dimensions
* [frmPlotViewer](frmPlotViewer.py): Window that can display, copy, save, and print a plot
* [frmRunSimulation](frmRunSimulation.py): Base for frmRunSWMM and frmRunEPANET, displays status while running model
* [help](help.py): Handle interactions with the Qt Help Assistant which displays help topics
* [highlighting](highlighting.py): Rules for syntax highlighting in script editor form
* [import_export](import_export.py): Import model elements from GIS layers and export model object to GIS layers
* [map_tools](map_tools.py): Implement tool buttons that interact with the map, put model object on the map
* [model_utility](model_utility.py): tree and list controls for main form, BasePlot for plotting data
* [property_editor_backend](property_editor_backend.py): populate property editor form and apply changes to model objects
* [settings](settings.py): set which language is displayed
* [text_plus_button](text_plus_button.py): combination of controls used in property editor to launch another editor

Resources:

* chinese.qm, qt_zh_CN.qm: Chinese internationalization
* french.qm, qt_fr.qm: French internationalization
* translations.qrc, translations_rc.py: translation resources
* svgs.qrc, svgs_rc.py: SVG icons that can be used on the map
* swmm.qrc, swmm_rc.py: icons for main form
