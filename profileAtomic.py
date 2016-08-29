"""
Profiling the ionisation rate equation solver.
"""
import cProfile, pstats

import numpy as np
import atomic

ntimes, ntemperatures = 50, 50

rt = atomic.RateEquations(atomic.element('carbon'))
times = np.logspace(-7, 1, ntimes)
temperature = np.logspace(0, 3, ntemperatures)
density = 1e19

cProfile.runctx("rt.solve(times, temperature, density)", globals(),
        locals(), "profile.prof")

s = pstats.Stats("profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
