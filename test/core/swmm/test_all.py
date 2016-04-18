import webbrowser
import unittest
from test.HTMLTestRunner import HTMLTestRunner
from test_title import SimpleTitleTest

# Options
from test_backdrop import SimpleBackdropTest
from test_options_dates import OptionsDatesTest
from test_options_dynamicwave import OptionsDynamicWaveTest
from test_files import SimpleFilesTest
from test_options_general import OptionsGeneralTest
from test_options_interfacefiles import OptionsInterfaceFilesTest
from test_map import SimpleMapTest
from test_report import SimpleReportTest
from test_options_timesteps import OptionsTimestepTest

# Climatology
from test_evaporation import SimpleEvaporationTest
from test_evaporation import ClimatologyEvaporationTest
from test_temperature import ClimatologyTemperatureTest
from test_adjustments import ClimatologyAdjustmentsTest

# Hydrology
from test_aquifers import SimpleAquifersTest
from test_aquifers import SingleAquiferTest
from test_lid_controls import SingleLIDControlTest
from test_raingages import SingleRainGageTest
from test_snowpack import SingleSnowPackTest
from test_subcatchments import SingleSubcatchmentTest
# -- Infiltrations
from test_groundwater import SingleGroundwaterTest
from test_lid_usage import SingleLIDUsageTest
from test_coverages import SingleCoverageTest
from test_coverages import MultiCoveragesTest
from test_loadings import SingleLoadingTest
from test_hydrographs import SingleHydrographTest
from test_hydrographs import SimpleHydrographsTest

# Hydraulics
# Link:
# Conduit
# Pump
# Orifice
# Weir
# Outlet
# Crosssection
# Transect
# Transects
from test_xsection import XsectionTest

# Node:
from test_junctions import SingleJunctionTest
from test_outfalls import SingleOutfallTest
from test_dividers import SingleDividerTest
# Storage
# Inflows - Direct Inflows
# DWf - dry weather inflow
# RDII - RDI inflow
# Treatment

# Quality:
from test_pollutants import SinglePollutantTest
from test_buildup import SingleBuildupTest
from test_washoff import SingleWashoffTest
from test_landuses import SingleLanduseTest

# Mislaneous
# from test_curves import SimpleCurveTest
# from test_labels import SimpleLableTest
# from test_energy import SimpleEnergyTest
# from test_patterns import SimplePatternTest
from test_project import ProjectTest
from test_title import SimpleTitleTest
from test_timeseries import SingleTimeSeriesTest

my_suite = unittest.TestSuite()

# Options
my_suite.addTest(SimpleBackdropTest())
my_suite.addTest(OptionsDatesTest())
my_suite.addTest(OptionsDynamicWaveTest())
my_suite.addTest(SimpleFilesTest())
my_suite.addTest(OptionsGeneralTest())
my_suite.addTest(OptionsInterfaceFilesTest())
my_suite.addTest(SimpleMapTest())
my_suite.addTest(SimpleReportTest())
my_suite.addTest(OptionsTimestepTest())

# Climatology
my_suite.addTest(SimpleEvaporationTest())
my_suite.addTest(ClimatologyEvaporationTest())
my_suite.addTest(ClimatologyTemperatureTest())
my_suite.addTest(ClimatologyAdjustmentsTest())

# Hydrology
my_suite.addTest(SimpleAquifersTest())
my_suite.addTest(SingleAquiferTest())
my_suite.addTest(SingleLIDControlTest())
my_suite.addTest(SingleRainGageTest())
my_suite.addTest(SingleSnowPackTest())
my_suite.addTest(SingleSubcatchmentTest())
# -- Place holder for infiltrations
my_suite.addTest(SingleGroundwaterTest())
my_suite.addTest(SingleLIDUsageTest())
my_suite.addTest(SingleCoverageTest())
my_suite.addTest(MultiCoveragesTest())
my_suite.addTest(SingleLoadingTest())
my_suite.addTest(SingleHydrographTest())
my_suite.addTest(SimpleHydrographsTest())

# Hydraulics
# Link:
# Conduit
# Pump
# Orifice
# Weir
# Outlet
# Crosssection
# Transect
# Transects
my_suite.addTest(XsectionTest())

# Node:
my_suite.addTest(SingleJunctionTest())
my_suite.addTest(SingleOutfallTest())
my_suite.addTest(SingleDividerTest())
# Storage
# Inflows - Direct Inflows
# DWf - dry weather inflow
# RDII - RDI inflow
# Treatment

# Quality:
my_suite.addTest(SinglePollutantTest())
my_suite.addTest(SingleBuildupTest())
my_suite.addTest(SingleWashoffTest())
my_suite.addTest(SingleLanduseTest())

# Mislaneous
my_suite.addTest(SimpleTitleTest())
my_suite.addTest(SingleTimeSeriesTest())
my_suite.addTest(ProjectTest())
# will need for later MTPs:
# my_suite.addTest(SimplePatternTest())
# my_suite.addTest(SimpleCurveTest())
# my_suite.addTest(SimpleLabelTest())


if __name__ == "__main__":
    # execute only if run as a script
    # runner = unittest.TextTestRunner()
    report_filename = "test_results_swmm.html"
    fp = file(report_filename, 'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title='SWMM Core Test Report',
        description='Unit test results')

    runner.run(my_suite)
    fp.close()
    try:
        webbrowser.open_new_tab(report_filename)
    except:
        print("Test results written to " + report_filename)
