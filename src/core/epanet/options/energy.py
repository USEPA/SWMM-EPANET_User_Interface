from core.epanet.patterns import Pattern
from core.inputfile import Section


class EnergyOptions(Section):
    """Defines global parameters used to compute pumping energy and cost"""

    SECTION_NAME = "[ENERGY]"

    @staticmethod
    def default():
        return EnergyOptions(EnergyOptions.SECTION_NAME, None, -1)

    def __init__(self, name, value, index):
        Section.__init__(self, name, value, None, index)
        # TODO: parse "value" argument to extract values for each field, after setting default values below
        # TODO: document valid values in docstrings below and/or implement each as an Enum or class

        self.global_price = 0.0		        # real
        """global default value of energy price for all pumps"""

        self.global_pattern	= Pattern      # pattern
        """global default value of price pattern for all pumps"""

        self.global_efficiency = 0.75		# real
        """global default value of pumping efficiency for all pumps"""

        self.demand_charge = 0.0		    # real
        """added cost per maximum kW usage during the simulation period"""
