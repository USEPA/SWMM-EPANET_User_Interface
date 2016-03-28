from core.epanet.options import energy
import unittest


class SimpleEnergyTest(unittest.TestCase):

    TEST_TEXT = (
        ("[ENERGY]\n"
         " Global Efficiency  \t82\n"
         " Global Price       \t1.5\n"
         " Demand Charge      \t3.4", "82", "1.5", "3.4"),
        ("[ENERGY]\n"
         " Global Efficiency  \t80\n"
         " Global Price       \t1.1\n"
         " Demand Charge      \t2.2", "80", "1.1", "2.2"),
        ("[ENERGY]\n"
         " Global Efficiency  \t75\n"
         " Global Price       \t0.0\n"
         " Demand Charge      \t0.0", "75", "0.0", "0.0"),
    )

    def runTest(self):

        for test_text in self.TEST_TEXT:
            my_energy = energy.EnergyOptions()
            my_energy.set_text(test_text[0])
            assert my_energy.global_efficiency == test_text[1]
            assert my_energy.global_price == test_text[2]
            assert my_energy.demand_charge == test_text[3]

        my_energy = energy.EnergyOptions()
        assert len(my_energy.get_text()) == 0

        my_energy.global_efficiency = "87.6"
        my_energy.global_price = "1.23"
        my_energy.demand_charge = "2.34"

        my_energy2 = energy.EnergyOptions()
        my_energy2.set_text(my_energy.get_text())

        assert my_energy2.matches(my_energy)
        assert my_energy2.global_efficiency == "87.6"
        assert my_energy2.global_price == "1.23"
        assert my_energy2.demand_charge == "2.34"

        expected_text = "[ENERGY]\n" + \
                        " Global Efficiency  	87.6\n" + \
                        " Global Price       	1.23\n" + \
                        " Demand Charge      	2.34"

        assert my_energy2.matches(expected_text)
