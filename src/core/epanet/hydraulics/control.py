from enum import Enum


class ControlType(Enum):
    """Control Type"""
    ABOVE = 1
    BELOW = 2
    TIME = 3
    CLOCKTIME = 4


class Control():
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

        self.clocktime = ""     # string
        """time of day (hour or hour:minute) AM/PM)"""

        self.control_type = ControlType.ABOVE
        """Simple controls are used to change link status or settings based on tank water level, junction pressure,
            time into the simulation or time of day"""

    def __str__(self):
        """Override default method to return string representation"""
        return self.get_text()

    def get_text(self):
        """format contents of this item for writing to file"""
        if self.link_id:
            prefix = " LINK " + self.link_id + ' ' + self.status
            if self.control_type == ControlType.ABOVE or self.control_type == ControlType.BELOW:
                return prefix + " IF NODE " + self.node_id + ' ' + self.control_type.name + ' ' + str(self.value)
            elif self.control_type == ControlType.TIME and len(self.time) > 0:
                return prefix + " AT TIME " + self.time
            elif self.control_type == ControlType.CLOCKTIME and len(self.clocktime) > 0:
                return prefix + " AT CLOCKTIME " + self.clocktime
        return ''

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        self.link_id, self.status = fields[1], fields[2]
        type_str = fields[4].upper()
        if type_str == "NODE":
            self.node_id = fields[5]
            self.control_type = ControlType[fields[6].upper()]
            self.value = fields[7]
        elif type_str == "TIME":
            self.control_type = ControlType.TIME
            self.time = fields[5]
        elif type_str == "CLOCKTIME":
            self.control_type = ControlType.CLOCKTIME
            self.clocktime = ' '.join(fields[5:])
        else:
            raise NameError("Unable to parse Control: " + new_text)
