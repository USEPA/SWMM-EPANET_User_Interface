from core.inputfile import InputFile, Section
from enum import Enum


class MapUnits(Enum):
    """Options for map units"""
    FEET = 1
    METERS = 2
    DEGREES = 3
    NONE = 4


class MapOptions(Section):
    """SWMM Map Options"""

    SECTION_NAME = "[MAP]"

    def __init__(self):
        Section.__init__(self)

        self.dimensions = (0.0, 0.0, 0.0, 0.0)  # real
        """
        Coordinates of the map extent:
        X1 lower-left X coordinate of full map extent
        Y1 lower-left Y coordinate of full map extent
        X2 upper-right X coordinate of full map extent
        Y2 upper-right Y coordinate of full map extent
        """

        self.units = MapUnits.FEET
        """map units"""

    def get_text(self):
        text_list = [MapOptions.SECTION_NAME]
        if self.dimensions:
            text_list.append(" {:17}\t{:16}\t{:16}\t{:16}\t{:16}".format("DIMENSIONS",
                             self.dimensions[0], self.dimensions[1], self.dimensions[2], self.dimensions[3]))
        if self.units:
            if isinstance(self.units, Enum):
                units_name = self.units.name
            else:
                units_name = str(self.units)
            text_list.append(" {:17}\t{}".format("UNITS", units_name))
        return '\n'.join(text_list)

    def set_text(self, new_text):
        MapOptions.__init__(self)
        for line in new_text.splitlines():
            try:
                if line.startswith(';'):
                    if self.comment:
                        self.comment += '\n'
                    self.comment += line
                if not line.startswith('['):
                    fields = line.split()
                    if len(fields) > 1:
                        if fields[0].lower() == "dimensions" and len(fields) > 4:
                            self.dimensions = fields[1:5]
                        else:
                            self.setattr_keep_type(InputFile.printable_to_attribute(fields[0]), fields[1])
            except:
                print("BackdropOptions skipping input line: " + line)
