from enum import Enum

import core.inputfile


class TimeSteps(core.inputfile.Section):
    """SWMM Time Step Options"""

    SECTION_NAME = "[OPTIONS]"

    # @staticmethod
    # def default():
    #     return Options(Options.SECTION_NAME, None, None, -1)

    def __init__(self):
        core.inputfile.Section.__init__(self)
        # TODO: parse "value" argument to extract values for each field, after setting default values below

        self.skip_steady_state = False
        """
        True to skip flow routing computations during steady state periods
        of a simulation. The last set of computed flows will be used.
        """

        self.report_step = "0:15:00"
        """Time interval for reporting of computed results"""

        self.wet_step = "0:05:00"
        """
        Time step length used to compute runoff from subcatchments during 
        periods of rainfall or when ponded water remains on the surface
        """

        self.dry_step = "1:00:00"
        """
        Time step length used for runoff computations 
        (consisting essentially of pollutant buildup) 
        during periods when there is no rainfall and no ponded water
        """

        self.routing_step = 600
        """
        Time step length in seconds used for routing flows and 
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