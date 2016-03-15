import traceback
from enum import Enum
from core.inputfile import Section


class CurveType(Enum):
    """Curve Type"""
    UNSET = 0
    PUMP = 1
    EFFICIENCY = 2
    VOLUME = 3
    HEADLOSS = 4


class Curves(Section):
    """CURVES section of EPANET input"""

    SECTION_NAME = "[CURVES]"

    def __init__(self):
        Section.__init__(self)
        self.comment = ";ID              \tX-Value     \tY-Value"

    def set_text(self, new_text):
        self.set_list_comment_plus_ids(new_text, Curve)


class Curve(Section):
    """Defines a data curve of X,Y points"""

    field_format = " {:16}\t{:12}\t{:12}\n"

    def __init__(self, new_text=None):
        self.curve_id = ''      # string
        """Curve ID Label"""

        self.description = ''   # string
        """Curve description"""

        self.curve_type = CurveType.UNSET    # PUMP, EFFICIENCY, VOLUME, or HEADLOSS
        """CurveType: Type of Curve"""

        self.curve_xy = []      # list of (x, y) tuples
        """X, Y Values"""

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        """format contents of this item for writing to file"""
        inp = ''
        if self.curve_type != CurveType.UNSET:
            inp += ";{}: {}\n".format(self.curve_type.name, self.description)
        elif self.description:
            inp += ";{}\n".format(self.description)
        for xy in self.curve_xy:
            inp += Curve.field_format.format(self.curve_id, xy[0], xy[1])
        return inp

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) == 2:
                # split curve type from description on colon and set
                colon_split = str.split(line, ':', 1)
                if len(colon_split) == 2:
                    try:
                        self.setattr_keep_type("curve_type", colon_split[0][1:].strip())
                    except Exception as e:
                        print("Curve could not set curve_type = " + colon_split[0][1:] + '\n' + str(e) + '\n' +
                              str(traceback.print_exc()))
                    self.description = colon_split[1].strip()
                else:
                    self.description = line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 2:
                    self.curve_id = fields[0]
                    self.curve_xy.append((fields[1], fields[2]))
