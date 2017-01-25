from enum import Enum
from core.project_base import Section
from core.metadata import Metadata


class PumpEnergyType(Enum):
    """Pump Energy Type"""
    PRICE = 1
    PATTERN = 2
    EFFICIENCY = 3


class EnergyOptions(Section):
    """Defines global parameters used to compute pumping energy and cost"""

    SECTION_NAME = "[ENERGY]"

    #    attribute,            input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("global_efficiency", "Global Efficiency"),
        ("global_price", "Global Price"),
        ("global_pattern", "Global Pattern"),
        ("demand_charge", "Demand Charge")))
    """Mapping between attribute name and name used in input file"""

    def __init__(self):
        Section.__init__(self)

        ## global default value of pumping efficiency for all pumps or efficiency curve name (percent)
        self.global_efficiency = "75"		# treat as string to preserve formatting

        ## global default value of energy price for all pumps
        self.global_price = "0.0"		    # str

        ## id of global default value of price pattern for all pumps
        self.global_pattern = ''            # str

        ## added cost per maximum kW usage during the simulation period
        self.demand_charge = "0.0"		    # str

        self.pumps = []

class PumpEnergy(Section):
    """Parameters used to compute pumping energy and cost for a particular pump"""

    def __init__(self):
        Section.__init__(self)

        ## Identifier of pump
        self.name = ''

        ## Indicator whether this pump energy specification is entered as price, pattern, or efficiency
        self.PricePatternEfficiency = PumpEnergyType.PRICE 	# PRICE, PATTERN, or EFFICIENCY

        # price, efficiency curve name, or pattern name is stored in self.value

