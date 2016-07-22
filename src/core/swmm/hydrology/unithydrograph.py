from core.inputfile import Section


class UnitHydrographEntry:
    def __init__(self, new_text=None):
        self.hydrograph_month = ''
        """str: Month for which hydrograph parameters will be defined"""

        self.term = ''
        """str: term of RDII response: SHORT or MEDIUM or LONG """

        self.response_ratio = ''
        """str: Parameter R"""

        self.time_to_peak = ''
        """str: Parameter T (hours)"""

        self.recession_limb_ratio = ''
        """str: Parameter K"""

        self.initial_abstraction_depth = ''
        """str: Maximum depth of initial abstraction available (Dmax)"""

        self.initial_abstraction_rate = ''
        """str: Rate at which any utilized initial abstraction is made available again (Drec)"""

        self.initial_abstraction_amount = ''
        """str: Amount of initial abstraction already utilized at the start of the simulation (D0)"""

class UnitHydrograph(Section):
    """Specifies the shapes of the triangular unit hydrographs that determine the amount of
        rainfall-dependent infiltration/inflow (RDII) entering the drainage system"""

    first_row_format = "{:16}\t{:16}"
    field_format = "{:16}\t{:16}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}"

    def __init__(self, new_text=None):
        Section.__init__(self)

        self.name = "Unnamed"
        """str: Name assigned to this Unit Hydrograph group"""

        self.rain_gage_id = ''
        """str: Name of the rain gage that supplies rainfall data to the unit hydrographs in the group"""

        self.value = []
        """UnitHydrographEntry: each active combination of parameters for this unit hydrograph"""

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        text_list = []

        if self.comment:
            text_list.append(self.comment)

        text_list.append(self.first_row_format.format(self.name, self.rain_gage_id))

        for entry in self.value:
            text_list.append(self.field_format.format(self.name,
                                                      entry.hydrograph_month,
                                                      entry.term,
                                                      entry.response_ratio,
                                                      entry.time_to_peak,
                                                      entry.recession_limb_ratio,
                                                      entry.initial_abstraction_depth,
                                                      entry.initial_abstraction_rate,
                                                      entry.initial_abstraction_amount))
        return '\n'.join(text_list)

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            entry = None
            line = self.set_comment_check_section(line)
            if line:
                fields = line.split()
                if self.name and self.name != "Unnamed" and self.name != fields[0]:
                    raise ValueError("UnitHydrograph.set_text: name: " + fields[0] + " != " + self.name + "\n"
                                     "in line: " + line)
                if len(fields) == 2:
                    (self.name, self.rain_gage_id) = fields
                elif len(fields) > 5:
                    entry = UnitHydrographEntry()
                    entry.hydrograph_month = fields[1]
                    entry.term = fields[2]
                    entry.response_ratio = fields[3]
                    entry.time_to_peak = fields[4]
                    entry.recession_limb_ratio = fields[5]
                    if len(fields) > 6:
                        entry.initial_abstraction_depth = fields[6]
                    if len(fields) > 7:
                        entry.initial_abstraction_rate = fields[7]
                    if len(fields) > 8:
                        entry.initial_abstraction_amount = fields[8]
                else:
                    print("UnitHydrograph.set_text skipped: " + line)
            if entry:
                self.value.append(entry)
