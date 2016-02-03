from core.epanet.patterns import Pattern
from core.inputfile import Section


class EnergyOptions(Section):
    """Defines global parameters used to compute pumping energy and cost"""

    SECTION_NAME = "[ENERGY]"

    def __init__(self):
        Section.__init__(self)

        self.global_price = 0.0		        # real
        """global default value of energy price for all pumps"""

        self.global_pattern = Pattern      # pattern
        """global default value of price pattern for all pumps"""

        self.global_efficiency = 75.0		# real
        """global default value of pumping efficiency for all pumps"""

        self.demand_charge = 0.0		    # real
        """added cost per maximum kW usage during the simulation period"""
