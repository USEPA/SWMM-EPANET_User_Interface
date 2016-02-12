class ControlRule:
    """Determines how pumps and regulators will be adjusted based on simulation time or conditions at
    specific nodes and links."""
    def __init__(self, name):
        self.ID = name
        """control rule id"""

        self.text = ""
        """text of control rule"""

