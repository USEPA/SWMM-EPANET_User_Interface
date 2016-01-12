from enum import Enum


class ControlType(Enum):
    """Control Type"""
    ABOVE = 1
    BELOW = 2
    TIME = 3
    CLOCK_TIME = 4


class Control:
    """Defines simple controls that modify links based on a single condition"""
    def __init__(self):
        self.simple_controls = SimpleControl   # collection of simple controls in the project
        """simple controls that modify links based on a single condition"""

        self.rule_based_controls = Rule   # collection of rule based controls
        """rule-based controls that modify links based on a combination of conditions"""


class SimpleControl:
    """Defines simple controls that modify links based on a single condition"""
    def __init__(self):
        self.link_ID = ""		# string
        """a link ID label"""

        self.status = ""	    # string
        """OPEN or CLOSED, a pump speed setting, or a control valve setting"""

        self.node_ID = ""		# string
        """a node ID label"""

        self.value = 0.0		# real
        """a pressure for a junction or a water level for a tank"""

        self.time = ""			# string
        """a time since the start of the simulation in decimal hours or in hours:minutes format"""

        self.clock_time = ""    # string
        """a 24-hour clock time (hours:minutes)"""

        self.control_type = ControlType.ABOVE
        """Simple controls are used to change link status or settings based on tank water level, junction pressure,
            time into the simulation or time of day"""


class Rule:
    """Defines rule-based controls that modify links based on a combination of conditions"""
    def __init__(self):
        self.RuleID = ""		    # string
        """an ID label assigned to the rule"""

        self.RuleText = ""		    # string
        """the text of the rule"""
