import unittest
from core.epanet.options import energy
from core.epanet.inp_reader_sections import EnergyOptionsReader
from core.epanet.inp_writer_sections import EnergyOptionsWriter
from test.core.section_match import match


class SimpleEnergyTest(unittest.TestCase):
    """Test Energy section"""
    TEST_TEXTS = (
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
         " Demand Charge      \t0.0", "75", "0.0", "0.0")
    )

    def test_reader_writer(self):
        """Test EnergyOptionsReader by comparing attributes values"""
        for test_text in self.TEST_TEXTS:
            my_energy = EnergyOptionsReader.read(test_text[0])
            assert my_energy.global_efficiency == test_text[1]
            assert my_energy.global_price == test_text[2]
            assert my_energy.demand_charge == test_text[3]
            actual_text = EnergyOptionsWriter.as_text(my_energy)
            msg = '\nSet:\n' + test_text[0] + '\nGet:\n' + actual_text
            self.assertTrue(match(actual_text, test_text[0]), msg)

    def test_writer(self):
        """Test EnergyOptionsWriter"""
        my_energy = energy.EnergyOptions()
        assert match(EnergyOptionsWriter.as_text(my_energy), SimpleEnergyTest.TEST_TEXTS[2][0])

        my_energy.global_efficiency = "87.6"
        my_energy.global_price = "1.23"
        my_energy.demand_charge = "2.34"

        actual_text1 = EnergyOptionsWriter.as_text(my_energy)

        my_energy2 = EnergyOptionsReader.read(actual_text1)
        actual_text2 = EnergyOptionsWriter.as_text(my_energy2)

        assert actual_text1 == actual_text2
        assert my_energy2.global_efficiency == "87.6"
        assert my_energy2.global_price == "1.23"
        assert my_energy2.demand_charge == "2.34"

        expected_text = "[ENERGY]\n" + \
                        " Global Efficiency  	87.6\n" + \
                        " Global Price       	1.23\n" + \
                        " Demand Charge      	2.34"

        msg = '\nSet:\n' + expected_text + '\nGet:\n' + actual_text2
        self.assertTrue(match(actual_text2, expected_text), msg)

    # def runTest(self):
    #     """Test set_text and get_text of energy options"""
    #     for test_text in self.TEST_TEXT:
    #         my_energy = energy.EnergyOptions()
    #         EnergyOptionsReader.read(test_text[0])
    #         assert my_energy.global_efficiency == test_text[1]
    #         assert my_energy.global_price == test_text[2]
    #         assert my_energy.demand_charge == test_text[3]
    #
    #     my_energy = energy.EnergyOptions()
    #     assert len(EnergyOptionsWriter.as_text(my_energy)) == 0
    #
    #     my_energy.global_efficiency = "87.6"
    #     my_energy.global_price = "1.23"
    #     my_energy.demand_charge = "2.34"
    #
    #     my_energy2 = energy.EnergyOptions()
    #     EnergyOptionsReader.read(EnergyOptionsWriter.as_text(my_energy2))
    #
    #     assert my_energy2.matches(my_energy)
    #     assert my_energy2.global_efficiency == "87.6"
    #     assert my_energy2.global_price == "1.23"
    #     assert my_energy2.demand_charge == "2.34"
    #
    #     expected_text = "[ENERGY]\n" + \
    #                     " Global Efficiency  	87.6\n" + \
    #                     " Global Price       	1.23\n" + \
    #                     " Demand Charge      	2.34"
    #
    #     assert my_energy2.matches(expected_text)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
