from enum import Enum
from core.project_base import Section


class ControlType(Enum):
    """Control Type"""
    ABOVE = 1
    BELOW = 2
    TIME = 3
    CLOCKTIME = 4


class Control(Section):
    """A simple control that modifies a link based on a single condition"""

    SECTION_NAME = "[CONTROLS]"

    """ Store section as string because that is how UI wants it. TODO: expand this class if parsing is needed. """
    def __init__(self):
        Section.__init__(self)

        ## Current value of the item as it appears in an InputFile
        self.value = ""

        ## A user-specified header and/or comment about the section
        self.comment = ""

        # self.name = ""		# string
        # """Name of link modified by this control"""
        #
        # self.status = ""	    # string
        # """OPEN or CLOSED, a pump speed setting, or a control valve setting"""
        #
        # self.node_name = ""		# string
        # """a node ID label"""
        #
        # self.value = 0.0		# real
        # """a pressure for a junction or a water level for a tank"""
        #
        # self.time = ""			# string
        # """a time since the start of the simulation in decimal hours or in hours:minutes format"""
        #
        # self.clocktime = ""     # string
        # """time of day (hour or hour:minute) AM/PM)"""
        #
        # self.control_type = ControlType.ABOVE
        # """Simple controls are used to change link status or settings based on tank water level, junction pressure,
        #     time into the simulation or time of day"""


class Rule(Section):
    """A simple control that modifies a link based on a single condition"""

    SECTION_NAME = "[RULES]"

    """ Store section as string because that is how UI wants it. TODO: expand this class if parsing is needed. """
    def __init__(self):
        Section.__init__(self)

        ## Current value of the item as it appears in an InputFile
        self.value = ""

        ## A user-specified header and/or comment about the section"
        self.comment = ""
