from core.swmm.hydraulics.link import Conduit
import unittest


class SingleConduitTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Conduit()

    def runTest(self):

        # Simple test examples
        # Predefined shapes with Geoms only
        test_text = r"""C2a              J2a              J2               157.48     0.016      4          4          0          0"""
        # --Test set_text
        # self.my_options.set_text(test_text)
        # --Test get_text through matches
        # actual_text = self.my_options.get_text()  # display purpose
        # assert self.my_options.matches(test_text)
        return False

class MultiConduitsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Conduit()

    def runTest(self):

        # Example 7
        test_text = """[CONDUITS]
        ;;               Inlet            Outlet                      Manning    Inlet      Outlet     Init.      Max.
        ;;Name           Node             Node             Length     N          Offset     Offset     Flow       Flow
        ;;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------
        C2a              J2a              J2               157.48     0.016      4          4          0          0
        C2               J2               J11              526.0      0.016      4          6          0          0
        C3               J3               J4               109.0      0.016      0          6          0          0
        C4               J4               J5               133.0      0.05       6          4          0          0
        C5               J5               J6               207.0      0.05       4          0          0          0
        C6               J7               J6               140.0      0.05       8          0          0          0
        C7               J6               J8               95.0       0.016      0          0          0          0
        C8               J8               J9               166.0      0.05       0          0          0          0
        C9               J9               J10              320.0      0.05       0          6          0          0
        C10              J10              J11              145.0      0.05       6          6          0          0
        C11              J11              O1               89.0       0.016      0          0          0          0
        C_Aux1           Aux1             J1               377.31     0.016      0          4          0          0
        C_Aux2           Aux2             J2a              239.41     0.016      0          4          0          0
        C_Aux1to2        J1               Aux2             286.06     0.016      4          0          0          0
        C_Aux3           Aux3             J3               444.75     0.05       6          0          0          0
        P1               J1               J5               185.39     0.016      0          0          0          0
        P2               J2a              J2               157.48     0.016      0          0          0          0
        P3               J2               J11              529.22     0.016      0          0          0          0
        P4               Aux3             J4               567.19     0.016      0          0          0          0
        P5               J5               J4               125.98     0.016      0          0          0          0
        P6               J4               J7               360.39     0.016      0          0          0          0
        P7               J7               J10              507.76     0.016      0          0          0          0
        P8               J10              J11              144.50     0.016      0          0          0          0
        """
        pass



