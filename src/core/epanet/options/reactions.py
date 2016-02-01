from core.inputfile import Section


class Reactions(Section):
    """Defines parameters related to chemical reactions occurring in the network"""

    SECTION_NAME = "[REACTIONS]"

    # @staticmethod
    # def default():
    #    return ReactionsOptions(ReactionsOptions.SECTION_NAME, None, -1)

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


