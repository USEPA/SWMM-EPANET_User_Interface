import core.swmm.hydraulics.node

import core.coordinates
import core.inputfile
import core.swmm.files
import core.swmm.hydraulics.link
import core.swmm.options
import core.swmm.raingage
import core.swmm.subcatchment


class Project(core.inputfile.InputFile):
    """Manage a complete SWMM input sequence"""

    section_types = {
        "[TITLE]": None,  # project title
        "[OPTIONS]": core.swmm.options.Options,  # analysis options
        "[REPORT]": None,  # output reporting instructions
        "[FILES]": core.swmm.files.Files,  # interface file options
        "[RAINGAGES]": [core.swmm.raingage.RainGage],  # rain gage information
        "[HYDROGRAPHS]": None,  # unit hydrograph data used to construct RDII inflows
        "[EVAPORATION]": None,  # evaporation data
        "[TEMPERATURE]": None,  # air temperature and snow melt data
        "[SUBCATCHMENTS]": [core.swmm.subcatchment.Subcatchment],  # basic subcatchment information
        "[SUBAREAS]": None,  # subcatchment impervious/pervious sub-area data
        "[INFILTRATION]": None,  # subcatchment infiltration parameters
        "[LID_CONTROLS]": None,  # low impact development control information
        "[LID_USAGE]": None,  # assignment of LID controls to subcatchments
        "[AQUIFERS]": None,  # groundwater aquifer parameters
        "[GROUNDWATER]": None,  # subcatchment groundwater parameters
        "[SNOWPACKS]": None,  # subcatchment snow pack parameters
        "[JUNCTIONS]": [core.swmm.hydraulics.node.JunctionNode],  # junction node information
        "[OUTFALLS]": None,  # outfall node information
        "[DIVIDERS]": None,  # flow divider node information
        "[STORAGE]": None,  # storage node information
        "[CONDUITS]": [core.swmm.hydraulics.link.Conduit],  # conduit link information
        "[PUMPS]": None,  # pump link information
        "[ORIFICES]": None,  # orifice link information
        "[WEIRS]": None,  # weir link information
        "[OUTLETS]": None,  # outlet link information
        "[XSECTIONS]": [core.swmm.hydraulics.link.CrossSection],  # conduit, orifice, and weir cross-section geometry
        "[TRANSECTS]": None,  # transect geometry for conduits with irregular cross-sections
        "[LOSSES]": None,  # conduit entrance/exit losses and flap valves
        "[CONTROLS]": None,  # rules that control pump and regulator operation
        "[POLLUTANTS]": None,  # pollutant information
        "[LANDUSES]": None,  # land use categories
        "[COVERAGES]": None,  # assignment of land uses to subcatchments
        "[BUILDUP]": None,  # buildup functions for pollutants and land uses
        "[WASHOFF]": None,  # washoff functions for pollutants and land uses
        "[TREATMENT]": None,  # pollutant removal functions at conveyance system nodes
        "[INFLOWS]": None,  # external hydrograph/pollutograph inflow at nodes
        "[DWF]": None,  # baseline dry weather sanitary inflow at nodes
        "[PATTERNS]": None,  # periodic variation in dry weather inflow
        "[RDII]": None,  # rainfall-dependent I/I information at nodes
        "[LOADINGS]": None,  # initial pollutant loads on subcatchments
        "[CURVES]": None,  # x-y tabular data referenced in other sections
        "[TIMESERIES]": None,  # time series data referenced in other sections

        "[MAP]": None,       # X,Y coordinates of the map's bounding rectangle
        "[POLYGONS]": None,  # X,Y coordinates for each vertex of subcatchment polygons
        "[COORDINATES]": [core.coordinates.Coordinates],  # X,Y coordinates for nodes
        "[VERTICES]": None,  # X,Y coordinates for each interior vertex of polyline links
        "[LABELS]": None,    # X,Y coordinates and text of labels
        "[SYMBOLS]": None,   # X,Y coordinates for rain gages
        "[BACKDROP]": None   # X,Y coordinates of the bounding rectangle and file name of the backdrop image.
        # [TAGS]
        }

    def __init__(self):
        self.section_types = Project.section_types
        core.inputfile.InputFile.__init__(self)



