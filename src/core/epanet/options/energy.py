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

        self.global_efficiency = "75"		# treat as string to preserve formatting
        """global default value of pumping efficiency for all pumps or efficiency curve ID (percent)"""

        self.global_price = "0.0"		    # str
        """global default value of energy price for all pumps"""

        self.global_pattern = ""            # str
        """id of global default value of price pattern for all pumps"""

        self.demand_charge = "0.0"		    # str
        """added cost per maximum kW usage during the simulation period"""

    def get_text(self):
        text = Section.get_text(self)
        if EnergyOptions().matches(text):
            return ''  # This section has nothing different from defaults, return blank
        else:
            return  text