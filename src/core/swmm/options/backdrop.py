from core.inputfile import InputFile, Section
from enum import Enum


class BackdropOptions(Section):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    def __init__(self):
        Section.__init__(self)

        self.dimensions = (0.0, 0.0, 0.0, 0.0)  # real
        """provides the X and Y coordinates of the lower-left and upper-right corners of the maps bounding rectangle"""

        self.file = "" 		                    # string
        """name of the file that contains the backdrop image"""

        self.units = ""      # "None"  # string
        self.offset = None   # (0.0, 0.0)  # real
        self.scaling = None  # (0.0, 0.0)  # real

    def get_text(self):
        text_list = [BackdropOptions.SECTION_NAME]
        if self.dimensions:
            text_list.append(" {:17}\t{:16}\t{:16}\t{:16}\t{:16}".format("DIMENSIONS",
                             self.dimensions[0], self.dimensions[1], self.dimensions[2], self.dimensions[3]))
        if self.units:
            text_list.append(" {:17}\t{}".format("UNITS", self.units))
        if self.file:
            text_list.append(" {:17}\t{}".format("FILE", self.file))
        if self.offset:
            text_list.append(" {:17}\t{:16}\t{:16}".format("OFFSET",
                             self.offset[0], self.offset[1]))
        if self.scaling:
            text_list.append(" {:17}\t{:16}\t{:16}".format("SCALING",
                             self.scaling[0], self.scaling[1]))
        return '\n'.join(text_list)

    def set_text(self, new_text):
        BackdropOptions.__init__(self)
        for line in new_text.splitlines():
            try:
                line = self.set_comment_check_section(line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].lower() == "dimensions" and len(fields) > 4:
                        self.dimensions = (float(fields[1]), float(fields[2]), float(fields[3]), float(fields[4]))
                    elif fields[0].lower() == "offset" and len(fields) > 2:
                        self.offset = (float(fields[1]), float(fields[2]))
                    elif fields[0].lower() == "scaling" and len(fields) > 2:
                        self.scaling = (float(fields[1]), float(fields[2]))
                    else:
                        self.setattr_keep_type(InputFile.printable_to_attribute(fields[0]), fields[1])
            except:
                print("BackdropOptions skipping input line: " + line)
