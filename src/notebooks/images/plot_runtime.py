import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp

S_MINUTE = 60
S_HOUR = S_MINUTE * 60
S_DAY = S_HOUR * 24
S_WEEK = S_DAY * 7
S_MONTH = S_DAY * 30
S_YEAR = S_MONTH * 12

# data in the form of simulation_minutes, runtime_seconds
# data extracted from Figure 9 https://arxiv.org/pdf/2212.05351.pdf
DATA = """
1, 0.732596542821523
60, 3.9318287557057703
1440, 99.99999999999959
44640, 3694.6012051992834
"""


def plot_runtime():
    # load data
    data = np.loadtxt(DATA.splitlines(), delimiter=',')
    simulation_seconds = data[:, 0] * 60
    runtime_seconds = data[:, 1]
    plt.figure(figsize=(5, 4.5))
    plt.plot(simulation_seconds, runtime_seconds, '-o')
    # make log-scale but using minutes, hours, days, months, years
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks([S_MINUTE, S_HOUR, S_DAY, S_MONTH, S_YEAR, S_YEAR * 10],
               ['1 min', '1 hr', '1 day', '1 mnth', '1 yr', '10 yr'])
    plt.yticks([1, S_MINUTE, S_HOUR, S_DAY, S_WEEK],
               ['1 s', '1 min', '1 hr', '1 day', '1 week'])
    plt.xlabel('Simulation time', fontdict=dict(size='x-large'))
    plt.ylabel('Runtime', fontdict=dict(size='x-large'))
    # increase major tick lenght
    ax = plt.gca()
    ax.tick_params(which='major', length=5)

    powerlaw = interp.interp1d(np.log(simulation_seconds[-3:]), np.log(runtime_seconds[-3:]), kind='linear',
                               fill_value='extrapolate')
    simulation_seconds_extrapolated = [S_MONTH, S_YEAR * 10]
    runtime_seconds_extrapolated = np.exp(powerlaw(np.log(simulation_seconds_extrapolated)))
    plt.plot(simulation_seconds_extrapolated, runtime_seconds_extrapolated, '--', color='tab:blue')

    plt.tight_layout()
    plt.savefig('runtime.png')


if __name__ == '__main__':
    plot_runtime()
