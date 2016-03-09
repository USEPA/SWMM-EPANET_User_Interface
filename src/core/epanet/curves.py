from enum import Enum
from core.inputfile import Section


class CurveType(Enum):
    """Curve Type"""
    PUMP = 1
    EFFICIENCY = 2
    VOLUME = 3
    HEADLOSS = 4


class Curves(Section):
    """CURVES section of EPANET input"""

    SECTION_NAME = "[CURVES]"

    def set_text(self, new_text):
        self.value = []
        lines = new_text.splitlines()
        first_curve = 1
        if str(lines[1]).startswith(';'):
            # Save first comment line as section comment
            self.comment = lines[1]
            first_curve += 1

        curve_text = ""
        curve_id = ""
        for line in lines[first_curve:]:
            if str(line).startswith(';'):
                if curve_text:
                    self.value.append(Curve(curve_text))
                curve_text = line
                curve_id = ""
            else:
                if len(curve_id) > 0:
                    id_split = new_text.split()
                    if id_split[0] != curve_id:
                        self.value.append(Curve(curve_text))
                        curve_text = ""
                        curve_id = ""
                if curve_text:
                    curve_text += '\n'
                curve_text += line

        if curve_text:
            self.value.append(Curve(curve_text))


class Curve(Section):
    """Defines a data curve of X,Y points"""

    field_format = " {:16}\t{:12}\t{:12}\n"

    def __init__(self, text=None):
        self.curve_id = ""      # string
        """Curve ID Label"""

        self.description = ""   # string
        """Curve description"""

        self.curve_type = CurveType.PUMP    # PUMP, EFFICIENCY, VOLUME, or HEADLOSS
        """CurveType: Type of Curve"""

        self.curve_xy = []      # list of (x, y) tuples
        """X, Y Values"""

        if text:
            self.set_text(text)

    def get_text(self):
        """format contents of this item for writing to file"""
        inp = ";{}: {}\n".format(self.curve_type.name, self.description)
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
                        print("Curve could not set curve_type = " + colon_split[0][1:] + '\n' + str(e))
                    self.description = colon_split[1].strip()
                else:
                    self.description = line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 2:
                    self.curve_id = fields[0]
                    self.curve_xy.append((fields[1], fields[2]))
