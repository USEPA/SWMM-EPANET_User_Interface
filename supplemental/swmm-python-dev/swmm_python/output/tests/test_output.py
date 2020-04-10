#
#   test_output.py
#
#   Created: 8/7/2018
#   Author: Michael E. Tryby
#           US EPA - ORD/NRMRL
#
#   Unit testing for SWMM Output API using pytest.
#
import os

import pytest
import numpy as np

from swmm.output import OutputMetadata
from swmm.output import output as smo

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
OUTPUT_FILE_EXAMPLE1 = os.path.join(DATA_PATH, 'Example1.out')


def test_openclose():
    _handle = smo.init()
    smo.open(_handle, OUTPUT_FILE_EXAMPLE1)
    smo.close(_handle)


@pytest.fixture()
def handle(request):
    _handle = smo.init()
    smo.open(_handle, OUTPUT_FILE_EXAMPLE1)

    def close():
        smo.close(_handle)

    request.addfinalizer(close)
    return _handle


def test_outputmetadata(handle):

    om = OutputMetadata(handle)

    ref = {
        smo.SubcatchAttribute.RAINFALL:           ("Rainfall",                "in/hr"),
        smo.SubcatchAttribute.SNOW_DEPTH:         ("Snow Depth",              "in"),
        smo.SubcatchAttribute.EVAP_LOSS:          ("Evaporation Loss",        "in/day"),
        smo.SubcatchAttribute.INFIL_LOSS:         ("Infiltration Loss",       "in/hr"),
        smo.SubcatchAttribute.RUNOFF_RATE:        ("Runoff Rate",             "cu ft/sec"),
        smo.SubcatchAttribute.GW_OUTFLOW_RATE:    ("Groundwater Flow Rate",   "cu ft/sec"),
        smo.SubcatchAttribute.GW_TABLE_ELEV:      ("Groundwater Elevation",   "ft"),
        smo.SubcatchAttribute.SOIL_MOISTURE:      ("Soil Moisture",           "%"),
        smo.SubcatchAttribute.POLLUT_CONC_0:      ("TSS",                     "mg/L"),
        smo.SubcatchAttribute.POLLUT_CONC_1:      ("Lead",                    "ug/L"),

        smo.NodeAttribute.INVERT_DEPTH:           ("Invert Depth",            "ft"),
        smo.NodeAttribute.HYDRAULIC_HEAD:         ("Hydraulic Head",          "ft"),
        smo.NodeAttribute.PONDED_VOLUME:          ("Ponded Volume",           "cu ft"),
        smo.NodeAttribute.LATERAL_INFLOW:         ("Lateral Inflow",          "cu ft/sec"),
        smo.NodeAttribute.TOTAL_INFLOW:           ("Total Inflow",            "cu ft/sec"),
        smo.NodeAttribute.FLOODING_LOSSES:        ("Flooding Loss",           "cu ft/sec"),
        smo.NodeAttribute.POLLUT_CONC_0:          ("TSS",                     "mg/L"),
        smo.NodeAttribute.POLLUT_CONC_1:          ("Lead",                    "ug/L"),

        smo.LinkAttribute.FLOW_RATE:              ("Flow Rate",               "cu ft/sec"),
        smo.LinkAttribute.FLOW_DEPTH:             ("Flow Depth",              "ft"),
        smo.LinkAttribute.FLOW_VELOCITY:          ("Flow Velocity",           "ft/sec"),
        smo.LinkAttribute.FLOW_VOLUME:            ("Flow Volume",             "cu ft"),
        smo.LinkAttribute.CAPACITY:               ("Capacity",                "%"),
        smo.LinkAttribute.POLLUT_CONC_0:          ("TSS",                     "mg/L"),
        smo.LinkAttribute.POLLUT_CONC_1:          ("Lead",                    "ug/L"),

        smo.SystemAttribute.AIR_TEMP:             ("Temperature",             "deg F"),
        smo.SystemAttribute.RAINFALL:             ("Rainfall",                "in/hr"),
        smo.SystemAttribute.SNOW_DEPTH:           ("Snow Depth",              "in"),
        smo.SystemAttribute.EVAP_INFIL_LOSS:      ("Evap and Infil Losses",   "in/hr"),
        smo.SystemAttribute.RUNOFF_FLOW:          ("Runoff Flow Rate",        "cu ft/sec"),
        smo.SystemAttribute.DRY_WEATHER_INFLOW:   ("Dry Weather Inflow",      "cu ft/sec"),
        smo.SystemAttribute.GW_INFLOW:            ("Groundwater Inflow",      "cu ft/sec"),
        smo.SystemAttribute.RDII_INFLOW:          ("RDII Inflow",             "cu ft/sec"),
        smo.SystemAttribute.DIRECT_INFLOW:        ("Direct Inflow",           "cu ft/sec"),
        smo.SystemAttribute.TOTAL_LATERAL_INFLOW: ("Total Lateral Inflow",    "cu ft/sec"),
        smo.SystemAttribute.FLOOD_LOSSES:         ("Flood Losses",            "cu ft/sec"),
        smo.SystemAttribute.OUTFALL_FLOWS:        ("Outfall Flow",            "cu ft/sec"),
        smo.SystemAttribute.VOLUME_STORED:        ("Volume Stored",           "cu ft"),
        smo.SystemAttribute.EVAP_RATE:            ("Evaporation Rate",        "in/day")
    }

    for attr in smo.SubcatchAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]

    for attr in smo.NodeAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]

    for attr in smo.LinkAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]

    for attr in smo.SystemAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]


def test_getversion(handle):

  assert smo.getversion(handle) == 51000


def test_getprojectsize(handle):

    assert smo.getprojectsize(handle) == [8, 14, 13, 2]


def test_getpollutantunits(handle):

    assert smo.getunits(handle)[2:] == [0, 1]


def test_getstartdate(handle):

    assert smo.getstartdate(handle) == 35796


def test_gettimes(handle):

    assert smo.gettimes(handle, smo.Time.NUM_PERIODS) == 36


def test_getelementname(handle):

    assert smo.getelementname(handle, smo.ElementType.NODE, 1) == "10"


def test_getsubcatchseries(handle):

    ref_array = np.array([0.0,
                          1.2438242,
                          2.5639679,
                          4.524055,
                          2.5115132,
                          0.69808137,
                          0.040894926,
                          0.011605669,
                          0.00509294,
                          0.0027438672])

    test_array = smo.getsubcatchseries(handle, 1, smo.SubcatchAttribute.RUNOFF_RATE, 0, 10)

    assert len(test_array) == 10
    assert np.allclose(test_array, ref_array)


def test_getsubcatchattribute(handle):

    ref_array = np.array([0.125,
                          0.125,
                          0.125,
                          0.125,
                          0.125,
                          0.225,
                          0.225,
                          0.225])

    test_array = smo.getsubcatchattribute(handle, 1, smo.SubcatchAttribute.INFIL_LOSS)

    assert len(test_array) == 8
    assert np.allclose(test_array, ref_array)


def test_getsubcatchresult(handle):

    ref_array = np.array([0.5,
                          0.0,
                          0.0,
                          0.125,
                          1.2438242,
                          0.0,
                          0.0,
                          0.0,
                          33.481991,
                          6.6963983])

    test_array = smo.getsubcatchresult(handle, 1, 1)

    assert len(test_array) == 10
    assert np.allclose(test_array, ref_array)


def test_getnoderesult(handle):

    ref_array = np.array([0.296234,
                          995.296204,
                          0.0,
                          1.302650,
                          1.302650,
                          0.0,
                          15.361463,
                          3.072293])

    test_array = smo.getnoderesult(handle, 2, 2)

    assert len(test_array) == 8
    assert np.allclose(test_array, ref_array)


def test_getlinkresult(handle):

    ref_array = np.array([4.631762,
                          1.0,
                          5.8973422,
                          314.15927,
                          1.0,
                          19.070757,
                          3.8141515])

    test_array = smo.getlinkresult(handle, 3, 3)

    assert len(test_array) == 7
    assert np.allclose(test_array, ref_array)


def test_getsystemresult(handle):

    ref_array = np.array([70.0,
                          0.1,
                          0.0,
                          0.19042271,
                          14.172027,
                          0.0,
                          0.0,
                          0.0,
                          0.0,
                          14.172027,
                          0.55517411,
                          13.622702,
                          2913.0793,
                          0.0])

    test_array = smo.getsystemresult(handle, 4, 4)

    assert len(test_array) == 14
    assert np.allclose(test_array, ref_array)
