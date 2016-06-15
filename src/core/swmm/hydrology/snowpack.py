from core.inputfile import Section


class SnowPack(Section):
    """Snow pack parameters"""

    LineTypes = (
        ("has_plowable",
         "PLOWABLE",
         "plowable_minimum_melt_coefficient",
         "plowable_maximum_melt_coefficient",
         "plowable_base_temperature",
         "plowable_fraction_free_water_capacity",
         "plowable_initial_snow_depth",
         "plowable_initial_free_water",
         "plowable_fraction_impervious_area"),
        ("has_impervious",
         "IMPERVIOUS",
         "impervious_minimum_melt_coefficient",
         "impervious_maximum_melt_coefficient",
         "impervious_base_temperature",
         "impervious_fraction_free_water_capacity",
         "impervious_initial_snow_depth",
         "impervious_initial_free_water",
         "impervious_depth_100_cover"),
        ("has_pervious",
         "PERVIOUS",
         "pervious_minimum_melt_coefficient",
         "pervious_maximum_melt_coefficient",
         "pervious_base_temperature",
         "pervious_fraction_free_water_capacity",
         "pervious_initial_snow_depth",
         "pervious_initial_free_water",
         "pervious_depth_100_cover"),
        ("has_removal",
         "REMOVAL",
         "depth_snow_removal_begins",
         "fraction_transferred_out_watershed",
         "fraction_transferred_impervious_area",
         "fraction_transferred_pervious_area",
         "fraction_converted_immediate_melt",
         "fraction_moved_another_subcatchment",
         "subcatchment_transfer"))

    def __init__(self, new_text=None):
        Section.__init__(self)

        self.name = ''
        """User-assigned name for this snow pack"""

        self.has_plowable = False
        self.has_impervious = False
        self.has_pervious = False
        self.has_removal = False

        self.plowable_minimum_melt_coefficient = "0.0"
        """Degree-day snow melt coefficient that occurs on December 21"""

        self.plowable_maximum_melt_coefficient = "0.0"
        """Degree-day snow melt coefficient that occurs on June 21"""

        self.plowable_base_temperature = "0.0"
        """Temperature at which snow begins to melt"""

        self.plowable_fraction_free_water_capacity = "0.0"
        """Volume of a snow pack's pore space which must fill with melted snow before liquid runoff from the
            pack begins, expressed as a fraction of snow pack depth"""

        self.plowable_initial_snow_depth = "0.0"
        """Depth of snow at the start of the simulation"""

        self.plowable_initial_free_water = "0.0"
        """Depth of melted water held within the pack at the start of the simulation"""

        self.plowable_fraction_impervious_area = "0.0"
        """Fraction of impervious area that is plowable and therefore is not subject to areal depletion"""

        self.impervious_minimum_melt_coefficient = "0.0"
        """Degree-day snow melt coefficient that occurs on December 21"""

        self.impervious_maximum_melt_coefficient = "0.0"
        """Degree-day snow melt coefficient that occurs on June 21"""

        self.impervious_base_temperature = "0.0"
        """Temperature at which snow begins to melt"""

        self.impervious_fraction_free_water_capacity = "0.0"
        """Volume of a snow pack's pore space which must fill with melted snow before liquid runoff from the
            pack begins, expressed as a fraction of snow pack depth"""

        self.impervious_initial_snow_depth = "0.0"
        """Depth of snow at the start of the simulation"""

        self.impervious_initial_free_water = "0.0"
        """Depth of melted water held within the pack at the start of the simulation"""

        self.impervious_depth_100_cover = "0.0"
        """Depth of snow beyond which the entire area remains completely covered and is not subject to
            any areal depletion effect"""

        self.pervious_minimum_melt_coefficient = "0.0"
        """Degree-day snow melt coefficient that occurs on December 21"""

        self.pervious_maximum_melt_coefficient = "0.0"
        """Degree-day snow melt coefficient that occurs on June 21"""

        self.pervious_base_temperature = "0.0"
        """Temperature at which snow begins to melt"""

        self.pervious_fraction_free_water_capacity = "0.0"
        """Volume of a snow pack's pore space which must fill with melted snow before liquid runoff from the
            pack begins, expressed as a fraction of snow pack depth"""

        self.pervious_initial_snow_depth = "0.0"
        """Depth of snow at the start of the simulation"""

        self.pervious_initial_free_water = "0.0"
        """Depth of melted water held within the pack at the start of the simulation"""

        self.pervious_depth_100_cover = "0.0"
        """Depth of snow beyond which the entire area remains completely covered and is not subject to
            any areal depletion effect"""

        self.depth_snow_removal_begins = "0.0"
        """Depth which must be reached before any snow removal begins"""

        self.fraction_transferred_out_watershed = "0.0"
        """Fraction of snow depth that is removed from the system"""

        self.fraction_transferred_impervious_area = "0.0"
        """Fraction of snow depth that is added to snow accumulation on the pack's impervious area"""

        self.fraction_transferred_pervious_area = "0.0"
        """Fraction of snow depth that is added to snow accumulation on the pack's pervious area"""

        self.fraction_converted_immediate_melt = "0.0"
        """Fraction of snow depth that becomes liquid water, runs onto any subcatchment associated with the snow pack"""

        self.fraction_moved_another_subcatchment = "0.0"
        """Fraction of snow depth which is added to the snow accumulation on some other subcatchment"""

        self.subcatchment_transfer = ""
        """subcatchment receiving transfers of snow depth"""

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        """format contents of this item for writing to file"""
        text_list = []
        if self.comment:
            text_list.append(self.comment)
        for field_names in self.LineTypes:
            if getattr(self, field_names[0]):               # If the flag for this group of fields is true,
                line = self.name + '\t' + field_names[1]    # add a line with name, group name,
                for field_name in field_names[2:]:          # and the field values in this group.
                    line += '\t' + str(getattr(self, field_name))
                text_list.append(line)
        return '\n'.join(text_list)

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            line = self.set_comment_check_section(line)
            if line:
                fields = line.split()
                if len(fields) > 2:
                    if not self.name:                      # If we have not found a name yet, use the first one we find
                        self.name = fields[0]
                    elif fields[0] != self.name:           # If we find a different name, complain
                        raise ValueError("SnowPack.set_text: name: " + fields[0] + " != " + self.name)
                    check_type = fields[1].upper()
                    found_type = False
                    for field_names in self.LineTypes:
                        if field_names[1].upper() == check_type:  # Find the group of fields this line is about
                            found_type = True
                            setattr(self, field_names[0], True)   # Set flag to show we have this group
                            for (field_name, field_value) in zip(field_names[2:], fields[2:]):
                                self.setattr_keep_type(field_name, field_value)
                            continue
                    if not found_type:
                        raise ValueError("SnowPack.set_text: Unknown line: " + line)
