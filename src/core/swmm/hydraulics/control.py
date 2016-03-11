# TODO: expand and use this class if needed. Currently swmm Project implements CONTROLS section as list of strings.


class ControlRule:
    """Determines how pumps and regulators will be adjusted based on simulation time or conditions at
    specific nodes and links."""
    def __init__(self, name):
        self.ID = name
        """control rule id"""

        self.rule_text = ""
        """text of control rule"""

