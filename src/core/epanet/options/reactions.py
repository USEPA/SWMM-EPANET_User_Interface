from core.inputfile import Section


class Reactions(Section):
    """Defines parameters related to chemical reactions occurring in the network"""

    SECTION_NAME = "[REACTIONS]"

    field_dict = {
        "Order Bulk": "order_bulk",
        "Order Tank": "order_wall",
        "Order Wall": "order_tank",
        "Global Bulk": "global_bulk",
        "Global Wall": "global_wall",
        "Limiting Potential": "limiting_potential",
        "Roughness Correlation": "roughness_correlation"}
    """Mapping from label used in file to field name"""

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

        def set_text(self, new_text):
            """Read properties from text.
                Args:
                    new_text (str): Text to parse into properties.
            """
            zero_pos = new_text.upper().find("ZERO")  # Replace "zero" with numeral if it appears, any capitalization
            if zero_pos >= 0:
                new_text = new_text[:zero_pos] + '0' + new_text[zero_pos + len("ZERO"):]
            Section.set_text(self, new_text)



