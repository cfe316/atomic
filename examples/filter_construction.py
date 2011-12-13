import numpy as np
import matplotlib.pyplot as plt

import atomic
from atomic.pec import filtered_atomic_data


def fetch_pec_data():
    from atomic.adas import OpenAdas
    db = OpenAdas()
    res = db.search_adf15('carbon')
    for r in res:
        db.fetch(r, 'adas_data/pec')


def plot_coeffs(ad, te, charge, **kwargs):
    ax = plt.gca()

    ne = 1e19

    label = kwargs.pop('label', True)
    coeff_line = ad.coeffs['line_power'](charge, te, ne)
    coeff_cont = ad.coeffs['continuum_power'](charge, te, ne)
    coeff_cx = ad.coeffs['cx_power'](charge, te, ne)

    if ax.lines != []:
        colors = [l.get_color() for l in ax.lines]
    else:
        colors = [''] * 3

    for i, key in enumerate(['line_power', 'continuum_power', 'cx_power']):
        if label:
            label_str = key
        else:
            label_str = None
        c= ad.coeffs[key](charge, te, ne)
        ax.loglog(te, c, colors[i], label=label_str, **kwargs)

    ax.set_ylabel('$P/n_\mathrm{e} n_\mathrm{I}\ [\mathrm{W m^3}]$')


if __name__ == '__main__':
    ad = atomic.element('carbon')
    ad_filtered = filtered_atomic_data(ad, 'adas_data/pec/pec96#c_pju*.dat')

    te = np.logspace(0, 3)

    f = plt.figure(1); f.clf()

    for i, charge in enumerate([1, 2, 5]):
        ax = f.add_subplot(3, 1, i+1)
        plot_coeffs(ad, te, charge)
        plot_coeffs(ad_filtered, te, charge, marker='x', ls='', label=None)
        ax.set_ylim(1e-35, 1e-30)
        label = '$\mathrm{%s}^{%d+}$' % (ad.element, charge)
        ax.text(0.02, 0.95, label, transform=ax.transAxes, va='top')

    ax.legend(loc='best')
    plt.draw()
    plt.show()
