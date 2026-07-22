"""
===============================================================================
myMDsim
-------------------------------------------------------------------------------

File
    box.py

Description
    Defines the simulation box and stores the geometrical information of the
    simulation domain.

Main class
    Box

Dependencies
    numpy

Notes
    The Box class only stores geometrical information.
    Boundary conditions are implemented independently in the boundaries module.

Author
    Guglielmo Mennella

===============================================================================
"""

import numpy as np

class Box:
    """
    Simulation box.

    Purpose
    -------
    Represents the geometry of the simulation domain.

    Responsibilities
    ----------------
    - store box dimensions
    - compute volume
    - provide geometrical utilities
    - remain independent of boundary conditions

    Notes
    -----
    Boundary conditions are intentionally implemented in another module so that
    different boundary conditions can operate on the same Box object.
    """

    def __init__(self, lengths_list):

        self._lentghs = lengths_list 