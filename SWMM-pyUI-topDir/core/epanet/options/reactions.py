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

        ## set the order of reactions occurring in the bulk fluid
        self.order_bulk = 1.0		    # real

        ## set the order of reactions occurring in the pipe wall
        self.order_wall = 1.0	        # real

        ## set the order of reactions occurring in the tanks
        self.order_tank = 1.0	        # real

        ## set a global value for all bulk reaction coefficients
        self.global_bulk = 0.0		    # real

        ## set a global value for all wall reaction coefficients
        self.global_wall = 0.0		    # real

        ## specifies that reaction rates are proportional to difference between concentration and potential value
        self.limiting_potential = 0.0	    # real

        ## make all default pipe wall reaction coefficients be related to pipe roughness
        self.roughness_correlation = 0.0    # real

        ## pipe/tank specific reaction coefficients
        self.value = []

