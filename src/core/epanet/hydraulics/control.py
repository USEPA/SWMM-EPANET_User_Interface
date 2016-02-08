from enum import Enum


class ControlType(Enum):
    """Control Type"""
    ABOVE = 1
    BELOW = 2
    TIME = 3
    CLOCK_TIME = 4


class Control:
    """A control modifies links"""
    def __init__(self):
        self.simple_controls = [SimpleControl]   # collection of simple controls in the project
        """simple controls that modify links based on a single condition"""

        self.rule_based_controls = [Rule]   # collection of rule based controls
        """rule-based controls that modify links based on a combination of conditions"""

    @property
    def text(self):
        """format contents of this item for writing to file"""
        return self.row

    @text.setter
    def text(self, new_text):
        self.row = new_text


class SimpleControl:
    """Defines simple controls that modify links based on a single condition"""
    def __init__(self):
        self.link_id = ""		# string
        """a link ID label"""

        self.status = ""	    # string
        """OPEN or CLOSED, a pump speed setting, or a control valve setting"""

        self.node_id = ""		# string
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

    @property
    def text(self):
        """format contents of this item for writing to file"""
        inp = " "
        if self.link_id:
            inp += "LINK " + self.link_id
        inp += self.status + ' '
        if self.node_id:
            inp += "NODE " + self.node_id + ' '
        if self.value:
            inp += self.control_type + ' ' + str(self.value) + ' '
        if self.time:
            inp += self.time + ' '
        if self.clock_time:
            inp += self.clock_time + ' '
        # TODO: research correct formatting of time, clock_time options
        return inp

    @text.setter
    def text(self, new_text):
        fields = new_text.split()
        self.link_id = fields[0]
        # TODO: Populate additional fields


class Rule:
    """Defines rule-based controls that modify links based on a combination of conditions"""
    def __init__(self):
        self.rule_id = ""		    # string
        """an ID label assigned to the rule"""

        self.rule_text = ""		    # string
        """the text of the rule"""

    @property
    def text(self):
        """format contents of this item for writing to file"""
        return self.rule_id + '\t' + self.rule_text

    @text.setter
    def text(self, new_text):
        (self.rule_id, self.rule_text) = new_text.split(None, 1)
