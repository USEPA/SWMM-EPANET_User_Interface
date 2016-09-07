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
from test_evaporation import EvaporationTest
from test_temperature import TemperatureTest
from test_adjustments import AdjustmentsTest

# Hydrology
from test_aquifers import SimpleAquifersTest
from test_lid_controls import SimpleLIDControlTest
from test_raingages import SimpleRainGageTest
from test_snowpack import SimpleSnowPackTest
from test_subcatchments import SimpleSubcatchmentTest
from test_infiltrations import InfiltrationTest
from test_groundwater import SimpleGroundwaterTest
from test_lid_usage import SimpleLIDUsageTest
from test_coverages import SimpleCoverageTest
from test_loadings import SimpleLoadingTest
from test_hydrographs import SimpleHydrographsTest

# Hydraulics
# Link:
from test_conduits import SimpleConduitTest
# Pump
# Orifice
# Weir
# Outlet
# CrossSection
from test_xsections import SimpleCrossSectionTest
from test_transects import SimpleTransectTest
from test_xsection import XsectionTest

# Node:
from test_junctions import SimpleJunctionTest
from test_outfalls import SimpleOutfallTest
from test_dividers import SimpleDividerTest

# Storage
from test_inflows import SimpleInflowTest
from test_dwf import SimpleDWITest
from test_RDII import SimpleRDIITest
from test_treatment import SimpleTreatmentTest

# Quality:
from test_pollutants import SimplePollutantTest
from test_buildup import SingleBuildupTest
from test_washoff import SimpleWashoffTest
from test_landuses import SimpleLanduseTest

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
from test_patterns import SimplePatternTest
from test_timeseries import SimpleTimeSeriesTest

# Mislaneous
# from test_energy import SimpleEnergyTest
from test_project import ProjectTest
from test_title import SimpleTitleTest

my_suite = unittest.TestSuite()

# Options
my_suite.addTest(SimpleBackdropTest('test_bare'))
my_suite.addTest(SimpleBackdropTest('test_backdrop'))
my_suite.addTest(SimpleBackdropTest('test_missing_value'))
my_suite.addTest(OptionsDatesTest())
my_suite.addTest(OptionsDynamicWaveTest())
my_suite.addTest(SimpleFilesTest('test_space_delimited'))
my_suite.addTest(SimpleFilesTest('test_more_space'))
my_suite.addTest(SimpleFilesTest('test_space_in_filename'))
my_suite.addTest(SimpleFilesTest('test_filename_with_path'))
my_suite.addTest(SimpleFilesTest('test_all_options'))
my_suite.addTest(SimpleFilesTest('test_interface_files'))
my_suite.addTest(OptionsGeneralTest('test_all_opts'))
my_suite.addTest(OptionsGeneralTest('test_current_text'))
my_suite.addTest(OptionsInterfaceFilesTest())
my_suite.addTest(SimpleMapTest("test_reader"))
my_suite.addTest(SimpleMapTest("test_writer"))
my_suite.addTest(SimpleReportTest("test_reader_writer"))
my_suite.addTest(SimpleReportTest("test_more"))
my_suite.addTest(OptionsTimestepTest())

# Climatology
my_suite.addTest(EvaporationTest("test_bare"))
my_suite.addTest(EvaporationTest("test_constant_only"))
my_suite.addTest(EvaporationTest("test_constant_wt_dry_only"))
my_suite.addTest(EvaporationTest("test_monthly"))
my_suite.addTest(EvaporationTest("test_monthly_fail"))
my_suite.addTest(EvaporationTest("test_timeseries"))
my_suite.addTest(EvaporationTest("test_temperature"))
my_suite.addTest(EvaporationTest("test_file"))
my_suite.addTest(EvaporationTest("test_recovery"))
my_suite.addTest(EvaporationTest('test_project_section'))

my_suite.addTest(TemperatureTest('test_default'))
my_suite.addTest(TemperatureTest('test_timeseries'))
my_suite.addTest(TemperatureTest('test_file'))
my_suite.addTest(TemperatureTest('test_file_wt_date'))
my_suite.addTest(TemperatureTest('test_windspeed_monthly'))
my_suite.addTest(TemperatureTest('test_windspeed_file_wt_temperature'))
my_suite.addTest(TemperatureTest('test_windspeed_file_fail'))
my_suite.addTest(TemperatureTest('test_snowmelt'))
my_suite.addTest(TemperatureTest('test_snowmelt_fail'))
my_suite.addTest(TemperatureTest('test_snowmelt_wo_adc'))
my_suite.addTest(TemperatureTest('test_snowmelt_wo_temperature'))
my_suite.addTest(AdjustmentsTest('test_default'))
my_suite.addTest(AdjustmentsTest('test_all_opts'))
my_suite.addTest(AdjustmentsTest('test_miss_col'))
my_suite.addTest(AdjustmentsTest('test_miss_row'))

# Hydrology
my_suite.addTest(SimpleAquifersTest('test_aquifer'))
my_suite.addTest(SimpleAquifersTest('test_aquifers'))
my_suite.addTest(SimpleLIDControlTest('test_lid_surface'))
my_suite.addTest(SimpleLIDControlTest('test_lid_control'))
my_suite.addTest(SimpleLIDControlTest('test_example4a'))
my_suite.addTest(SimpleRainGageTest('test_one_raingage'))
my_suite.addTest(SimpleRainGageTest('test_raingage_section'))
my_suite.addTest(SimpleSnowPackTest('test_one_pack'))
my_suite.addTest(SimpleSnowPackTest('test_one_type'))
my_suite.addTest(SimpleSnowPackTest('test_snowpacks_section'))
my_suite.addTest(SimpleSubcatchmentTest('test_pk'))
my_suite.addTest(SimpleSubcatchmentTest('test_nopk'))
my_suite.addTest(SimpleSubcatchmentTest('test_missing'))
my_suite.addTest(SimpleSubcatchmentTest('test_subcatchments'))
my_suite.addTest(InfiltrationTest('test_horton'))
my_suite.addTest(InfiltrationTest('test_greenampt'))
my_suite.addTest(InfiltrationTest('test_curvenumber'))
my_suite.addTest(InfiltrationTest('test_horton_infiltration_section'))
my_suite.addTest(InfiltrationTest('test_greenampt_infiltration_section'))
my_suite.addTest(InfiltrationTest('test_curvenumber_infiltration_section'))
my_suite.addTest(SimpleGroundwaterTest('test_groundwater'))
my_suite.addTest(SimpleGroundwaterTest('test_groundwater_section'))
my_suite.addTest(SimpleLIDUsageTest('test_lid_usage'))
my_suite.addTest(SimpleLIDUsageTest('test_lid_usage_section'))
my_suite.addTest(SimpleCoverageTest('test_coverage'))
my_suite.addTest(SimpleCoverageTest('test_default_coverages'))
my_suite.addTest(SimpleCoverageTest('test_coverages'))
my_suite.addTest(SimpleLoadingTest('test_one_loading'))
my_suite.addTest(SimpleLoadingTest('test_loading_section'))
my_suite.addTest(SimpleHydrographsTest('test_hydrograph'))
my_suite.addTest(SimpleHydrographsTest('test_hydrographs'))

# Hydraulics
# Link:
my_suite.addTest(SimpleConduitTest('test_conduit'))
my_suite.addTest(SimpleConduitTest('test_conduit_section'))
# MTP3 Pump
# MTP3 Orifice
# MTP3 Weir
my_suite.addTest(SimpleCrossSectionTest('test_geom'))
my_suite.addTest(SimpleCrossSectionTest('test_geom_barrel'))
my_suite.addTest(SimpleCrossSectionTest('test_geom_barrel_culvert'))
my_suite.addTest(SimpleCrossSectionTest('test_custom_curve'))
my_suite.addTest(SimpleCrossSectionTest('test_custom_curve_barrelnum'))
my_suite.addTest(SimpleCrossSectionTest('test_irregular_tsectnum'))
my_suite.addTest(SimpleCrossSectionTest('test_xsections_section'))
my_suite.addTest(XsectionTest())

my_suite.addTest(SimpleTransectTest('test_one_transect'))
my_suite.addTest(SimpleTransectTest('test_transects'))
my_suite.addTest(SimpleTransectTest('test_transect_section'))

# Node:
my_suite.addTest(SimpleJunctionTest('test_all_opts'))
my_suite.addTest(SimpleJunctionTest('test_selected_parameters'))
my_suite.addTest(SimpleJunctionTest('test_junctions'))
my_suite.addTest(SimpleOutfallTest('test_one_outfall'))
my_suite.addTest(SimpleOutfallTest('test_outfall_section'))
my_suite.addTest(SimpleDividerTest('test_overflow_divider'))
my_suite.addTest(SimpleDividerTest('test_cutoff_divider'))
my_suite.addTest(SimpleDividerTest('test_tabular_divider'))
my_suite.addTest(SimpleDividerTest('test_weir_divider'))
my_suite.addTest(SimpleDividerTest('test_dividers'))

# Storage
my_suite.addTest(SimpleInflowTest('test_flow_type'))
my_suite.addTest(SimpleInflowTest('test_mass_type'))
my_suite.addTest(SimpleInflowTest('test_flow_ts_type'))
my_suite.addTest(SimpleInflowTest('test_inflows_flow'))
my_suite.addTest(SimpleInflowTest('test_inflows_flowts'))
my_suite.addTest(SimpleDWITest('test_example3'))
my_suite.addTest(SimpleDWITest('test_example8'))
my_suite.addTest(SimpleDWITest('test_dwf_section_example3'))
my_suite.addTest(SimpleDWITest('test_dwf_section_example8'))
my_suite.addTest(SimpleRDIITest('test_one_rdii'))
my_suite.addTest(SimpleRDIITest('test_rdii_section'))
my_suite.addTest(SimpleTreatmentTest('test_bod'))
my_suite.addTest(SimpleTreatmentTest('test_lead'))
my_suite.addTest(SimpleTreatmentTest('test_treatment_section'))

# Quality:
my_suite.addTest(SimplePollutantTest('test_one_pollutant'))
my_suite.addTest(SimplePollutantTest('test_pollutant_section'))
my_suite.addTest(SingleBuildupTest('test_buildup'))
my_suite.addTest(SingleBuildupTest('test_buildup_section'))
my_suite.addTest(SimpleWashoffTest('test_one_washoff'))
my_suite.addTest(SimpleWashoffTest('test_washoff_section'))
my_suite.addTest(SimpleLanduseTest('test_default'))
my_suite.addTest(SimpleLanduseTest('test_all_opts'))
my_suite.addTest(SimpleLanduseTest('test_landuses'))

# Mislaneous
my_suite.addTest(SimpleTitleTest('test_bare'))
my_suite.addTest(SimpleTitleTest('test_empty'))
my_suite.addTest(SimpleTitleTest('test_empty_wo_return'))
my_suite.addTest(SimpleTitleTest('test_one_row_wt_return'))
my_suite.addTest(SimpleTitleTest('test_multiple_lines'))
my_suite.addTest(SimpleTitleTest('test_return_before_title'))

my_suite.addTest(SimpleTimeSeriesTest('test_file'))
my_suite.addTest(SimpleTimeSeriesTest('test_data'))
my_suite.addTest(SimpleTimeSeriesTest('test_multiple_lines'))
my_suite.addTest(SimpleTimeSeriesTest('test_timeseries_section'))

# will need for later MTPs:
my_suite.addTest(SimplePatternTest('test_hourly'))
my_suite.addTest(SimplePatternTest('test_daily'))
my_suite.addTest(SimplePatternTest('test_monthly'))
my_suite.addTest(SimplePatternTest('test_weekly'))
my_suite.addTest(SimplePatternTest('test_design'))
my_suite.addTest(SimplePatternTest('test_pattern_section'))
my_suite.addTest(SimpleCurveTest('test_storage_curve'))
my_suite.addTest(SimpleCurveTest('test_pump_curve'))
my_suite.addTest(SimpleCurveTest('test_curves_section'))
# my_suite.addTest(SimpleLabelTest())

# Project moved as seperate regression test
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
