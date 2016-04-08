from core.inputfile import Section
from core.metadata import Metadata

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

        self.global_efficiency = "75"		# treat as string to preserve formatting
        """global default value of pumping efficiency for all pumps or efficiency curve ID (percent)"""

        self.global_price = "0.0"		    # str
        """global default value of energy price for all pumps"""

        self.global_pattern = ''            # str
        """id of global default value of price pattern for all pumps"""

        self.demand_charge = "0.0"		    # str
        """added cost per maximum kW usage during the simulation period"""

    def get_text(self):
        if self.global_efficiency != "75" \
           or self.global_price != "0.0" \
           or self.global_pattern != '' \
           or self.demand_charge != "0.0":
            return Section.get_text(self)
        else:
            return ''  # This section has nothing different from defaults, return blank
