# SWMM and EPANET User Interface Source Code

Each form may have three files: 
- <form name>Designer.ui: file saved by Qt Designer specifying the layout of controls
- <form name>Designer.py: Python code automatically generated from the .ui file
- <form name>.py: Python code handling the form's behavior and interaction with the main program

Folders:

* EPANET, SWMM: model-specific forms and behavior

Files:

* chinese.qm, qt_zh_CN.qm: Chinese internationalization
* [convenience.py](convenience.py): Methods for interacting with Qt controls
* editor.py: Script editor form
* embed_ipython_new.py: Not in use, was for using iPython script editor
* french.qm, qt_fr.qm: French internationalization
* frmGenericListOutput: Display for a grid of data
* frmGenericPropertyEditor: Display and allow editing of properties
* frmMain: Main form base class for frmMainEPANET and frmMainSWMM
* frmMapAddVector: Form for adding a vector layer from a GIS file (not in use)
* frmMapDimensions: Form for editing map dimensions
* frmPlotViewer: Window that can display, copy, save, and print a plot
* frmRunSimulation: Base for frmRunSWMM and frmRunEPANET, displays status while running model
* help.py: Handle interactions with the Qt Help Assistant which displays help topics
* highlighting.py: Rules for syntax highlighting in script editor form
* import_export.py: Import model elements from GIS layers and export model object to GIS layers
* map_tools.py: Implement tool buttons that interact with the map, put model object on the map
* model_utility.py: tree and list controls for main form, BasePlot for plotting data
* property_editor_backend.py: populate property editor form and apply changes to model objects
* settings.py: set which language is displayed
* svgs.qrc, svgs_rc.py: SVG icons that can be used on the map
* swmm.qrc, swmm_rc.py: icons for main form
* text_plus_button.py: combination of controls used in property editor to launch another editor
* translations.qrc, translations_rc.py: internationalization resources
