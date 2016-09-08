# This piece of physics comes from Post's 1995 paper
# "Calculations of Energy Losses due to Atomic Processes in
#  Tokamaks with Applications to the ITER Divertor"
# 
# we determine Equation 2's integral.
# 
# For starters, let's calculate Lz at a constant density,
# and at tau=infinity.

import numpy as np

import atomic
import scipy.integrate

def temperatureRange(ad, top=1e3):
    """Get the temperature range to integrate for an element.
    
    We expect recombination at around half the
    first ionisation energy, so the integral should be from there upwards.
    """
    first_ion=ad.coeffs['ionisation_potential'](0,10,1e19)
    return np.logspace(np.log10(first_ion/2.0), np.log10(top),200)

def post_integral(ad, temperature, electron_density):
    """\int_0^{Tes} Lz(Te) Te^{1/2} \;dTe    
    
    Lz is given in W m^3 so the output has units of [W m^3 eV^{1/2}]
    """
    eq = atomic.CollRadEquilibrium(ad)
    y = eq.ionisation_stage_distribution(temperature, electron_density)
    Lz = atomic.Radiation(y).specific_power['total']
    Lzint = scipy.integrate.cumtrapz(Lz * np.sqrt(temperature), x=temperature, initial=0)
    return Lzint

def rhs(ad, temperature, electron_density):
    """The rhs of Post's equation (2). 
    
    He is using Lz in units of ergs cm^3 s.
    One of those equals 10^{-13} W m^3.
    
    """
    lzint = post_integral(ad, temperature, electron_density)
    return 2.5e5 * np.sqrt(temperature ** 2 * (lzint * 1e13) )
