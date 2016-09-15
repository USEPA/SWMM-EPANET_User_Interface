from core.project_base import Section


class Controls(Section):
    SECTION_NAME = "[CONTROLS]"

    """ Store section as string because that is how UI wants it. TODO: expand this class if parsing is needed. """
    def __init__(self):
        """Initialize or reset section"""
        Section.__init__(self)

        self.value = ""
        """Current value of the item as it appears in an InputFile"""

        self.comment = ""
        """A user-specified header and/or comment about the section"""

    def setattr_keep_type(self, attr_name, attr_value):
        # Not currently setting any attributes for this section
        pass

# class ControlRule:
#     """Determines how pumps and regulators will be adjusted based on simulation time or conditions at
#     specific nodes and links."""
#     def __init__(self, name):
#         self.name = name
#         """control rule id"""
#
#         self.rule_text = ""
#         """text of control rule"""
