from core.project_base import Section
from core.metadata import Metadata


class Events(Section):
    """Events"""

    SECTION_NAME = "[EVENTS]"

    # DEFAULT_COMMENT = ";;Start Date         End Date"

    #    attribute,            input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("start_date", "START DATE"),
        ("start_time", "START TIME"),
        ("end_date", "END DATE"),
        ("end_time", "END Time")))

    def __init__(self):
        Section.__init__(self)

        self.name = ""

        ## start date
        self.start_date = "01/01/1900"

        ## start time
        self.start_time = "00:00"

        ## end date
        self.end_date = "12/31/2000"

        ## end time
        self.end_time = "23:00"


