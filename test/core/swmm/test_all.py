##  This section is needed to run coverage from the command line ------TODO: change
## >> Run coverage from command line, navigate to test_all.py
## >> coverage run test_all.py
## >> coverage report >> Report_coverage_SWMM.txt
# import sys
# sp = sorted(sys.path)
# dnames = ', '.join(sp)
# print(dnames)
# sys.path.append("E:\\Code\\PyCharmProjects\\SWMM-EPANET_User_Interface")
# sys.path.append("E:\\Code\\PyCharmProjects\\SWMM-EPANET_User_Interface\\src")
# -------------------------------------------------------------------
import webbrowser
import unittest
from test.HTMLTestRunner import HTMLTestRunner

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
from test_evaporation import EvaporationTest
from test_temperature import ClimatologyTemperatureTest
from test_adjustments import AdjustmentsTest

# Hydrology
from test_aquifers import SimpleAquifersTest
from test_lid_controls import SingleLIDControlTest
from test_raingages import SingleRainGageTest
from test_snowpack import SingleSnowPackTest
from test_subcatchments import SingleSubcatchmentTest
from test_infiltrations import SingleHortonInfiltrationTest
from test_infiltrations import SingleGreenAmptInfiltrationTest
from test_infiltrations import SingleCurveNumberInfiltrationTest
from test_groundwater import SingleGroundwaterTest
from test_lid_usage import SingleLIDUsageTest
from test_coverages import SimpleCoverageTest
from test_loadings import SingleLoadingTest
from test_hydrographs import SingleHydrographTest
from test_hydrographs import SimpleHydrographsTest

# Hydraulics
# Link:
# Conduit
from test_conduits import SimpleConduitTest
# Pump
# Orifice
# Weir
# Outlet
# CrossSection
from test_xsections import SingleCrossSectionTest
from test_transects import SingleTransectTest
from test_transects import MultipleTransectsTest
from test_xsection import XsectionTest

# Node:
from test_junctions import SingleJunctionTest
from test_outfalls import SingleOutfallTest
from test_dividers import SimpleDividerTest
# Storage
from test_inflows import SingleInflowTest
from test_dwf import SimpleDWITest
from test_RDII import SingleRDIITest
from test_treatment import SingleTreatmentTest

# Quality:
from test_pollutants import SinglePollutantTest
from test_buildup import SingleBuildupTest
from test_washoff import SingleWashoffTest
from test_landuses import SingleLanduseTest

# Map related:
# -- Map is in options group
# Coordinates
# Vertices
# Polygons
# Symbols
# Labels
# from test_labels import SimpleLableTest
# -- Backdrop is in options group

# Mislaneous relations:
from test_curves import SimpleCurveTest
# Hydrographs is moved to Hydrology section
from test_patterns import SinglePatternTest
from test_timeseries import SingleTimeSeriesTest

# Mislaneous
# from test_energy import SimpleEnergyTest
from test_project import ProjectTest
from test_title import SimpleTitleTest

my_suite = unittest.TestSuite()

# Options
my_suite.addTest(SimpleBackdropTest('test_bare'))
my_suite.addTest(SimpleBackdropTest('test_backdrop'))
# my_suite.addTest(SimpleBackdropTest('test_missing_value'))
my_suite.addTest(OptionsDatesTest())
my_suite.addTest(OptionsDynamicWaveTest())
my_suite.addTest(SimpleFilesTest('test_space_delimited'))
my_suite.addTest(SimpleFilesTest('test_more_space'))
my_suite.addTest(SimpleFilesTest('test_space_in_filename'))
my_suite.addTest(SimpleFilesTest('test_filename_with_path'))
my_suite.addTest(SimpleFilesTest('test_all_options'))
my_suite.addTest(OptionsGeneralTest())
my_suite.addTest(OptionsInterfaceFilesTest())
my_suite.addTest(SimpleMapTest())
my_suite.addTest(SimpleReportTest())
my_suite.addTest(OptionsTimestepTest())

# Climatology
my_suite.addTest(SimpleEvaporationTest())
# my_suite.addTest(ClimatologyEvaporationTest())
my_suite.addTest(EvaporationTest("test_bare"))
my_suite.addTest(EvaporationTest("test_constant_only"))
my_suite.addTest(EvaporationTest("test_constant_wt_dry_only"))
my_suite.addTest(EvaporationTest("test_monthly"))
my_suite.addTest(EvaporationTest("test_monthly_fail"))
my_suite.addTest(EvaporationTest("test_timeseries"))
my_suite.addTest(EvaporationTest("test_temperature"))
my_suite.addTest(EvaporationTest("test_file"))
my_suite.addTest(EvaporationTest("test_recovery"))

my_suite.addTest(ClimatologyTemperatureTest())
my_suite.addTest(AdjustmentsTest('test_default'))
my_suite.addTest(AdjustmentsTest('test_all_opts'))
my_suite.addTest(AdjustmentsTest('test_miss_col'))
my_suite.addTest(AdjustmentsTest('test_miss_row'))

# Hydrology
my_suite.addTest(SimpleAquifersTest('test_aquifer'))
my_suite.addTest(SimpleAquifersTest('test_aquifers'))
my_suite.addTest(SingleLIDControlTest())
my_suite.addTest(SingleRainGageTest())
my_suite.addTest(SingleSnowPackTest())
my_suite.addTest(SingleSubcatchmentTest())
my_suite.addTest(SingleHortonInfiltrationTest())
my_suite.addTest(SingleGreenAmptInfiltrationTest())
my_suite.addTest(SingleCurveNumberInfiltrationTest())
my_suite.addTest(SingleGroundwaterTest())
my_suite.addTest(SingleLIDUsageTest())
my_suite.addTest(SimpleCoverageTest('test_coverage'))
my_suite.addTest(SimpleCoverageTest('test_default_coverages'))
my_suite.addTest(SimpleCoverageTest('test_coverages'))
my_suite.addTest(SingleLoadingTest())
my_suite.addTest(SingleHydrographTest())
my_suite.addTest(SimpleHydrographsTest())

# Hydraulics
# Link:
# my_suite.addTest(SimpleConduitTest('test_conduit'))
# my_suite.addTest(SimpleConduitTest('test_conduit_section'))
# Pump
# Orifice
# Weir
# Outlet
my_suite.addTest(SingleCrossSectionTest())
my_suite.addTest(SingleTransectTest())
my_suite.addTest(MultipleTransectsTest())
my_suite.addTest(XsectionTest())

# Node:
my_suite.addTest(SingleJunctionTest())
my_suite.addTest(SingleOutfallTest())
# my_suite.addTest(SimpleDividerTest('test_overflow_divider'))
# my_suite.addTest(SimpleDividerTest('test_cutoff_divider'))
# my_suite.addTest(SimpleDividerTest('test_tabular_divider'))
# my_suite.addTest(SimpleDividerTest('test_weir_divider'))
# my_suite.addTest(SimpleDividerTest('test_dividers'))

# Storage
my_suite.addTest(SingleInflowTest())
my_suite.addTest(SimpleDWITest('test_example3'))
my_suite.addTest(SimpleDWITest('test_example8'))
my_suite.addTest(SimpleDWITest('test_dwf_section_example3'))
my_suite.addTest(SimpleDWITest('test_dwf_section_example8'))
my_suite.addTest(SingleRDIITest())
my_suite.addTest(SingleTreatmentTest())

# Quality:
my_suite.addTest(SinglePollutantTest())
my_suite.addTest(SingleBuildupTest('test_buildup'))
my_suite.addTest(SingleBuildupTest('test_buildup_section'))
my_suite.addTest(SingleWashoffTest())
my_suite.addTest(SingleLanduseTest())

# Mislaneous
my_suite.addTest(SimpleTitleTest())
my_suite.addTest(SingleTimeSeriesTest())
# will need for later MTPs:
my_suite.addTest(SinglePatternTest())
my_suite.addTest(SimpleCurveTest('test_storage_curve'))
my_suite.addTest(SimpleCurveTest('test_pump_curve'))
my_suite.addTest(SimpleCurveTest('test_curves_section'))
# my_suite.addTest(SimpleLabelTest())
# my_suite.addTest(ProjectTest())

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
