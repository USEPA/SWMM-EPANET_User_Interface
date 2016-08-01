from core.project_base import Section
from core.metadata import Metadata


class Reactions(Section):
    """Defines parameters related to chemical reactions occurring in the network"""

    SECTION_NAME = "[REACTIONS]"

    #    attribute,               input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("order_bulk",            "Order Bulk"),
        ("order_wall",            "Order Wall"),
        ("order_tank",            "Order Tank"),
        ("global_bulk",           "Global Bulk"),
        ("global_wall",           "Global Wall"),
        ("limiting_potential",    "Limiting Potential"),
        ("roughness_correlation", "Roughness Correlation")))
    """Mapping between attribute name and name used in input file"""

    def __init__(self):
        Section.__init__(self)

        self.order_bulk = 1.0		    # real
        """set the order of reactions occurring in the bulk fluid"""

        self.order_wall = 1.0		    # real
        """set the order of reactions occurring in the pipe wall"""

        self.order_tank = 1.0	        # real
        """set the order of reactions occurring in the tanks"""

        self.global_bulk = 0.0		    # real
        """set a global value for all bulk reaction coefficients"""

        self.global_wall = 0.0		    # real
        """set a global value for all wall reaction coefficients"""

        self.limiting_potential = 0.0	    # real
        """specifies that reaction rates are proportional to difference between concentration and potential value"""

        self.roughness_correlation = 0.0    # real
        """make all default pipe wall reaction coefficients be related to pipe roughness"""

    # def get_text(self):
    #     """format contents of this item for writing to file"""
    #     if self.comment and self.comment.upper().startswith(";TYPE"):
    #         # TODO: implement reactions table as list of reactions
    #         return self.value
    #     else:
    #         return Section.get_text(self)

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        self.__init__()
        # Replace "zero" (any capitalization) with numeral 0
        zero_pos = new_text.upper().find("ZERO")
        while zero_pos >= 0:
            new_text = new_text[:zero_pos] + '0' + new_text[zero_pos + len("ZERO"):]
            zero_pos = new_text.upper().find("ZERO", zero_pos)
        for line in new_text.splitlines():
            upper_line = line.upper().strip()
            if upper_line.startswith("BULK") or upper_line.startswith("WALL") or upper_line.startswith("TANK"):
                self.comment += '\n' + line  # TODO: parse into table of per pipe values
            else:
                self.set_text_line(line)

