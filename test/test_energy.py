from core.epanet.options import energy
import unittest


class SimpleEnergyTest(unittest.TestCase):

    TEST_TEST = (
        ("[ENERGY]\n"
         " Global Efficiency  \t82\n"
         " Global Price       \t1.5\n"
         " Demand Charge      \t3.4", 82.0, 1.5, 3.4),
        ("[ENERGY]\n"
         " Global Efficiency  \t80\n"
         " Global Price       \t1.1\n"
         " Demand Charge      \t2.2", 80.0, 1.1, 2.2),
        ("[ENERGY]\n"
         " Global Efficiency  \t75\n"
         " Global Price       \t0.0\n"
         " Demand Charge      \t0.0", 75.0, 0.0, 0.0),
    )

    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_energy = energy.EnergyOptions()

    def runTest(self):
        for test_text in self.TEST_TEST:
            self.my_energy = energy.EnergyOptions()
            self.my_energy.text = test_text[0]
            assert self.my_energy.global_efficiency == test_text[1]
            assert self.my_energy.global_price == test_text[2]
            assert self.my_energy.demand_charge == test_text[3]

        my_energy2 = energy.EnergyOptions()
        my_energy2.global_efficiency = 87.6
        my_energy2.global_price = 1.23
        my_energy2.demand_charge = 2.34

        my_energy3 = energy.EnergyOptions()
        my_energy3.text = my_energy2.text
        assert my_energy3.global_efficiency == 87.6
        assert my_energy3.global_price == 1.23
        assert my_energy3.demand_charge == 2.34
