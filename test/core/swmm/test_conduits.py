import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydraulics.link import Conduit


class SimpleConduitTest(unittest.TestCase):
    """Test CONDUIT section, MTP3"""

    def test_conduit(self):
        """Test one set of conduit parameters"""
        self.my_options = Conduit()
        # Predefined shapes with Geoms only
        test_text = r"""C2a   J2a   J2   157.48     0.016  4  4  0  0"""
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_conduit_section(self):
        """Test CONDUIT section using Project class, data from Example 7"""
        from_text = Project()
        source_text = "[CONDUITS]\n" \
                      " ;;               Inlet            Outlet                      Manning    Inlet      Outlet     Init.      Max.\n" \
                      " ;;Name           Node             Node             Length     N          Offset     Offset     Flow       Flow\n" \
                      " ;;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------\n" \
                      " C2a              J2a              J2               157.48     0.016      4          4          0          0\n" \
                      " C2               J2               J11              526.0      0.016      4          6          0          0\n" \
                      " C3               J3               J4               109.0      0.016      0          6          0          0\n" \
                      " C4               J4               J5               133.0      0.05       6          4          0          0\n" \
                      " C5               J5               J6               207.0      0.05       4          0          0          0\n" \
                      " C6               J7               J6               140.0      0.05       8          0          0          0\n" \
                      " C7               J6               J8               95.0       0.016      0          0          0          0\n" \
                      " C8               J8               J9               166.0      0.05       0          0          0          0\n" \
                      " C9               J9               J10              320.0      0.05       0          6          0          0\n" \
                      " C10              J10              J11              145.0      0.05       6          6          0          0\n" \
                      " C11              J11              O1               89.0       0.016      0          0          0          0\n" \
                      " C_Aux1           Aux1             J1               377.31     0.016      0          4          0          0\n" \
                      " C_Aux2           Aux2             J2a              239.41     0.016      0          4          0          0\n" \
                      " C_Aux1to2        J1               Aux2             286.06     0.016      4          0          0          0\n" \
                      " C_Aux3           Aux3             J3               444.75     0.05       6          0          0          0\n" \
                      " P1               J1               J5               185.39     0.016      0          0          0          0\n" \
                      " P2               J2a              J2               157.48     0.016      0          0          0          0\n" \
                      " P3               J2               J11              529.22     0.016      0          0          0          0\n" \
                      " P4               Aux3             J4               567.19     0.016      0          0          0          0\n" \
                      " P5               J5               J4               125.98     0.016      0          0          0          0\n" \
                      " P6               J4               J7               360.39     0.016      0          0          0          0\n" \
                      " P7               J7               J10              507.76     0.016      0          0          0          0\n" \
                      " P8               J10              J11              144.50     0.016      0          0          0          0"
        from_text.set_text(source_text)
        project_section = from_text.conduits
        assert Section.match_omit(project_section.get_text(), source_text, " \t-;\n")




