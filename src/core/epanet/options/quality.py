from enum import Enum

from core.project_base import Section


class QualityAnalysisType(Enum):
    """Type of Water Quality Analysis"""
    NONE = 1
    CHEMICAL = 2
    AGE = 3
    TRACE = 4


class QualityOptions(Section):
    """EPANET Quality Options"""

    SECTION_NAME = "[OPTIONS]"

    def __init__(self):
        Section.__init__(self)

        self.quality = QualityAnalysisType.NONE
        """Type of water quality analysis to perform"""

        self.chemical_name = ""
        """Name of chemical to be analyzed in quality section"""

        self.mass_units = ""
        """Units of chemical to be analyzed in quality section"""

        self.diffusivity = 1.0
        """Molecular diffusivity of the chemical being analyzed relative to that of chlorine in water"""

        self.trace_node = ""
        """Node id to use in a quality trace"""

        self.tolerance = 0.0
        """Difference in water quality level below one parcel of water is essentially the same as another"""

        #things to come for multispecies
        self.AREA_UNITS = 'M2'
        """Surface concentration is mass/m2"""
        self.RATE_UNITS = 'HR'
        """Reaction rates are concentration/hour"""
        self.SOLVER = 'RK5'
        """5-th order Runge-Kutta integrator"""
        self.TIMESTEP = 360
        """360 sec (5 min) solution time step"""
        self.RTOL = 0.001
        """Relative concentration tolerance"""
        self.ATOL = 0.0001
        """Absolute concentration tolerance"""

class QualitySpecies:
    """EPANET Quality Species"""
    def __init__(self):
        self.quality = QualityAnalysisType.NONE
        """Type of water quality analysis to perform"""
        self.name = ""
        """common name"""
        self.chemical_name = self.name
        """Chemical name"""
        self.mass_units = ""
        """Units of chemical to be analyzed in quality section"""

class QualityEquation:
    const_ka = 10.0
    const_kb = 0.1
    const_k1 = 5.0
    const_k2 = 1.0
    const_smax = 50

    @classmethod
    def rate_oxidation(cls):
        return QualityEquation.const_ka
    @classmethod
    def rate_decay(cls):
        return QualityEquation.const_kb
    @classmethod
    def coef_adsorption(cls):
        return QualityEquation.const_k1
    @classmethod
    def coef_desorption(cls):
        return QualityEquation.const_k2
    @classmethod
    def limit_adsorption(cls):
        return QualityEquation.const_smax

    def __init__(self, aEq):
        self.Equ = aEq

    def calculate(self, *args):
        pass

