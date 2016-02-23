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

    def get_text(self):
        text_list = [BackdropOptions.SECTION_NAME]
        if self.dimensions:
            text_list.append(" {:17}\t{:16}\t{:16}\t{:16}\t{:16}".format("DIMENSIONS",
                             self.dimensions[0], self.dimensions[1], self.dimensions[2], self.dimensions[3]))
        if self.file:
            text_list.append(" {:17}\t{}".format("FILE", self.file))
        return '\n'.join(text_list)

    def set_text(self, new_text):
        BackdropOptions.__init__(self)
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
