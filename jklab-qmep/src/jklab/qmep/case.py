# ==========================================================
# qmep_case.py
#
# QMEP case representation.
#
# ==========================================================

from dataclasses import dataclass
from pathlib import Path

from . import constants_qmep as qc

# ==========================================================

@dataclass(frozen=True)
class Case:

    N: int
    age: int
    epst: float

    @property
    def N_label(self):

        return f"N{self.N}"


    @property
    def age_label(self):

        return f"age{self.age}"


    @property
    def epst_int(self):

        return qc.epst_to_int(
            self.epst
        )


    @property
    def epst_label(self):

        return qc.epst_to_label(
            self.epst
        )
    

    @property
    def case_label(self):

        return (
            Path(self.N_label)
            / self.age_label
            / self.epst_label
        )
    

