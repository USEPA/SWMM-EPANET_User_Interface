from core.inputfile import Section


class Files(Section):
    """Optional SWMM interface file names to use or save during a run"""

    SECTION_NAME = "[FILES]"

    def __init__(self):
        Section.__init__(self)
        self.use_rainfall = None
        """Name of rainfall data file to use"""

        self.save_rainfall = None
        """Name of rainfall data file to save"""

        self.use_runoff = None
        """Name of runoff data file to use"""

        self.save_runoff = None
        """Name of runoff data file to save"""

        self.use_hotstart = None
        """Name of hot start data file to use"""

        self.save_hotstart = None
        """Name of hot start data file to save"""

        self.use_rdii = None
        """Name of RDII data file to use"""

        self.save_rdii = None
        """Name of RDII data file to save"""

        self.use_inflows = None
        """Name of inflows data file to use"""

        self.save_outflows = None
        """Name of outflows data file to save"""

