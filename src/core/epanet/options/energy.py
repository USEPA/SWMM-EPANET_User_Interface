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

        self.global_efficiency = "75"		# treat as string to preserve formatting
        """global default value of pumping efficiency for all pumps or efficiency curve ID (percent)"""

        self.global_price = "0.0"		    # str
        """global default value of energy price for all pumps"""

        self.global_pattern = ''            # str
        """id of global default value of price pattern for all pumps"""

        self.demand_charge = "0.0"		    # str
        """added cost per maximum kW usage during the simulation period"""

        self.pumps = []

    def get_text(self):
        if self.global_efficiency == "75" \
           and self.global_price == "0.0" \
           and self.global_pattern == '' \
           and self.demand_charge == "0.0" \
           and len(self.pumps) == 0:
            return ''  # This section has nothing different from defaults, return blank
        else:
            txt = [Section.get_text(self)]
            for pump_energy in self.pumps:      # Add text for each pump energy
                txt.append(pump_energy.get_text())
            return '\n'.join(txt)

    def set_text(self, new_text):
        self.__init__()
        Section.set_text(self, new_text)    # Initialize, and set the global values using metadata
        for line in new_text.splitlines():  # Set pump-specific values
            first_field = new_text.split(None, 1)[0]
            if first_field.upper() == "PUMP":
                self.pumps.append(PumpEnergy(line))


class PumpEnergy(Section):
    """Parameters used to compute pumping energy and cost for a particular pump"""

    field_format = "PUMP {:16}\t{:8}\t{}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            self.id = ''
            """Identifier of pump"""

            self.PricePatternEfficiency = PumpEnergyType.PRICE 	# PRICE, PATTERN, or EFFICIENCY
            """Indicator whether this pump energy specification is entered as price, pattern, or efficiency"""

            """price, efficiency curve id, or pattern id is stored in self.value"""

    def get_text(self):
        """format contents of this item for writing to file"""
        if len(self.id) > 0:
            return self.field_format.format(self.id,
                                            self.PricePatternEfficiency.name,
                                            self.value,
                                            self.comment)
        elif self.comment:
            return self.comment

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 3:
            self.id = fields[1]
            self.PricePatternEfficiency = PumpEnergyType[fields[2].upper()]
            self.value = fields[3]
