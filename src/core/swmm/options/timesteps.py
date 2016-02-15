import core.inputfile


class TimeSteps(core.inputfile.Section):
    """SWMM Time Step Options"""

    SECTION_NAME = "[OPTIONS]"

    field_dict = {
     "COMPATIBILITY": "",
     "REPORT_CONTROLS": "",
     "REPORT_INPUT": "",

     "SKIP_STEADY_STATE": "skip_steady_state",

     "REPORT_STEP": "report_step",
     "WET_STEP": "wet_step",
     "DRY_STEP": "dry_step",
     "ROUTING_STEP": "routing_step",

     "INERTIAL_DAMPING": "",
     "NORMAL_FLOW_LIMITED": "",
     "FORCE_MAIN_EQUATION": "",
     "VARIABLE_STEP": "",
     "LENGTHENING_STEP": "",
     "MIN_SURFAREA": "",
     "MAX_TRIALS": "",
     "HEAD_TOLERANCE": "",
     "SYS_FLOW_TOL": "sys_flow_tol",
     "LAT_FLOW_TOL": "lat_flow_tol",
     "MINIMUM_STEP": "",
     "THREADS": ""}
    """Mapping from label used in file to field name"""

    def __init__(self):
        core.inputfile.Section.__init__(self)

        self.skip_steady_state = False
        """bool: True to skip flow routing computations during steady state periods
            of a simulation. The last set of computed flows will be used.
        """

        self.report_step = "0:15:00"
        """str: Time interval for reporting of computed results."""

        self.wet_step = "0:05:00"
        """str: Time step length used to compute runoff from subcatchments during
        periods of rainfall or when ponded water remains on the surface.
        """

        self.dry_step = "1:00:00"
        """str: Time step length used for runoff computations
        (consisting essentially of pollutant buildup) 
        during periods when there is no rainfall and no ponded water.
        """

        self.routing_step = ""
        """str: Time step used for routing flows and
        water quality constituents through the conveyance system
        """

        self.sys_flow_tol = 5
        """
        Undocumented but shows up in SWMM 5 UI as 'system flow tolerance'
        """

        self.lat_flow_tol = 5
        """
        Undocumented but shows up in SWMM 5 UI as 'lateral flow tolerance'
        """