from atomic_data import AtomicData
from collisional_radiative import CollRadEquilibrium
from time_dependent_rates import RateEquations, RateEquationsWithDiffusion
from radiation import Radiation
from electron_cooling import ElectronCooling
from post_integral import rhs

element = AtomicData.from_element

