from core.project_base import Section
from core.metadata import Metadata


class Files(Section):
    """Optional SWMM interface file names to use or save during a run"""

    SECTION_NAME = "[FILES]"

    DEFAULT_COMMENT = ";;Interfacing Files"

    #    attribute,       input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("use_rainfall",  "USE RAINFALL"),
        ("save_rainfall", "SAVE RAINFALL"),
        ("use_runoff",    "USE RUNOFF"),
        ("save_runoff",   "SAVE RUNOFF"),
        ("use_hotstart",  "USE HOTSTART"),
        ("save_hotstart", "SAVE HOTSTART"),
        ("use_rdii",      "USE RDII"),
        ("save_rdii",     "SAVE RDII"),
        ("use_inflows",   "USE INFLOWS"),
        ("save_outflows", "SAVE OUTFLOWS")))
    """Mapping between attribute name and name used in input file"""

    def __init__(self):
        Section.__init__(self)

        ## Name of rainfall data file to use
        self.use_rainfall = None

        ## Name of rainfall data file to save
        self.save_rainfall = None

        ## Name of runoff data file to use
        self.use_runoff = None

        ## Name of runoff data file to save
        self.save_runoff = None

        ## Name of hot start data file to use
        self.use_hotstart = None

        ## Name of hot start data file to save
        self.save_hotstart = None

        ## Name of RDII data file to use
        self.use_rdii = None

        ## Name of RDII data file to save
        self.save_rdii = None

        ## Name of inflows data file to use
        self.use_inflows = None

        ## Name of outflows data file to save
        self.save_outflows = None
