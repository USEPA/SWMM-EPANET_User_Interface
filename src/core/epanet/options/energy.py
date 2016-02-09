from core.inputfile import Section


class EnergyOptions(Section):
    """Defines global parameters used to compute pumping energy and cost"""

    SECTION_NAME = "[ENERGY]"

    field_dict = {
        "Global Efficiency": "global_efficiency",
        "Global Price": "global_price",
        "Global Pattern": "global_pattern",
        "Demand Charge": "demand_charge"}
    """Mapping from label used in file to field name"""

    def __init__(self):
        Section.__init__(self)

        self.global_efficiency = "75"		# real or string; usually treat as string
        """global default value of pumping efficiency for all pumps or efficiency curve ID (percent)"""

        self.global_price = 0.0		        # real
        """global default value of energy price for all pumps"""

        self.global_pattern = ""            # string
        """id of global default value of price pattern for all pumps"""

        self.demand_charge = 0.0		    # real
        """added cost per maximum kW usage during the simulation period"""
