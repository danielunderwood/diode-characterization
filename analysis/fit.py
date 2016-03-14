"""
Fitting code for diode characterization lab
"""

from numpy import exp
from numpy import sqrt
from numpy import diag
from numpy import linspace
from numpy import sum
from scipy.optimize import curve_fit
from argparse import ArgumentParser
from data import get_data
from matplotlib.pyplot import plot as matplotlib_plot
from matplotlib.pyplot import show as maptlotlib_show
from matplotlib.pyplot import errorbar as matplotlib_errorbar
from matplotlib.pyplot import xlim
from matplotlib.pyplot import ylim
from matplotlib.pyplot import xlabel
from matplotlib.pyplot import ylabel
from matplotlib.pyplot import savefig
from matplotlib.pyplot import legend
from scipy.special import lambertw


# Constants (SI Units)
ELECTRON_CHARGE = 1.602176608 * 10 ** -19
SIGMA_ELECTRON_CHARGE = 9.8 * 10 ** -28

BOLTZMANN_CONSTANT = 1.38064852 * 10 ** -23
SIGMA_BOLTZMANN =  7.9 * 10 ** -30

# Temperature (Kelvin) to use for simple_model. Somewhere around room temperature
TEMPERATURE = 300
SIGMA_TEMPERATURE = 0


def simple_model(V, I0, alpha):
    """
    Simple model for diode IV curve using ideal diode equation

    @param V: Voltage (Independent variable)
    @param I0: Reverse Saturation Current (Parameter)
    @param alpha: Fit coefficient (Parameter)
    @return: Current based on this model with given parameters and voltage
    """

    return I0 * (exp(alpha * V) - 1)


def lambert_model(V, mu, eta):
    """
    Model for diodes using lambert W function

    @param V: Voltage
    @param mu: Fit parameter
    @param eta: Fit parameter
    @return: Fit evaluated at V with parameters mu and eta
    """

    return mu * lambertw(eta * V)


def fit_data(data, errors, model=simple_model):
    """
    Fits data to model

    @param data: Data to fit in (V, I) tuple
    @param errors: Errors for data
    @param model: Model to use. Defaults to simple_model
    @return: Fit parameters array
    """

    return curve_fit(model, xdata=data[0], ydata=data[1], sigma=errors, p0=[0, 10], maxfev=1000)


def n_from_alpha(alpha, sigma_alpha):
    """
    Gets the value of n from alpha

    @param alpha: Fit parameter alpha for simple_model
    @param sigma_alpha: Error for alpha from simple model
    @return: Tuple of float value of n and the uncertainty
    """

    n = ELECTRON_CHARGE / (alpha * BOLTZMANN_CONSTANT * TEMPERATURE)

    # Calculate the error for sigma
    sigma_n = 0
    sigma_n += (SIGMA_ELECTRON_CHARGE / (alpha * BOLTZMANN_CONSTANT * TEMPERATURE)) ** 2
    sigma_n += ELECTRON_CHARGE * (sigma_alpha / alpha) ** 2
    sigma_n += ELECTRON_CHARGE * (SIGMA_BOLTZMANN / BOLTZMANN_CONSTANT) ** 2
    sigma_n += ELECTRON_CHARGE * (SIGMA_TEMPERATURE / TEMPERATURE) ** 2
    sigma_n = sqrt(sigma_n)

    return (n, sigma_n)


def get_current_errors(V, R, sigma_V, sigma_R):
    """
    Get the current errors for given parameters

    @param V: Voltage for error
    @param R: Resistance for error
    @param sigma_V: Voltage error
    @param sigma_R: Resistance error
    @return: Sigma for current
    """

    return [sqrt((sigma_V / R) ** 2 + (v * sigma_R / R ** 2) ** 2) for v in V]


if __name__ == '__main__':
    # Set up argument parser
    parser = ArgumentParser(description='Load and fit data file for diode characterization')
    parser.add_argument('resistance', type=float)
    parser.add_argument('sigma_V', type=float)
    parser.add_argument('sigma_R', type=float)
    parser.add_argument('--output', type=str)
    parser.add_argument('--open-plot', dest='open_plot', action='store_true')
    parser.add_argument('filename', type=str)

    # Parse arguments
    parsed_args = parser.parse_args()
    resistance = parsed_args.resistance
    sigma_V = parsed_args.sigma_V
    sigma_R = parsed_args.sigma_R
    output_filename = parsed_args.output
    open_plot = parsed_args.open_plot
    data_filename = parsed_args.filename

    # Get and parse data
    data = get_data(data_filename)
    currents = [voltage / resistance for voltage in data['resistor1_voltage']]
    voltages = [voltage for voltage in data['dut_voltage']]
    data_tuple = (voltages, currents)
    errors = get_current_errors(voltages, resistance, sigma_V, sigma_R)

    # Fit data and get errors
    params, covars = fit_data(data_tuple, errors, model=simple_model)
    sigmas = sqrt(diag(covars))

    I0 = params[0]
    sigma_I0 = sigmas[0]

    alpha = params[1]
    sigma_alpha = sigmas[1]

    # Get n
    n, sigma_n = n_from_alpha(alpha, sigma_alpha)

    # Create points for data to plot
    fit_V = linspace(min(voltages), max(voltages), 1000)
    fit_I = [simple_model(V, I0, alpha) for V in fit_V]

    # Chi squared and reduced chi squared
    degrees_of_freedom = len(currents) - len(params) - 1
    chi_squared = sum((simple_model(voltages[i], I0, alpha) - currents[i]) ** 2 / errors[i] **2
                      for i, _ in enumerate(voltages))
    reduced_chi_squared = chi_squared / degrees_of_freedom

    # Print results
    print('I0: %E +/- %E' % (I0, sigma_I0))
    print('alpha: %E +/- %E' % (alpha, sigma_alpha))
    print('n: %E +/- %E' % (n, sigma_n))
    print('Chi Squared: %f' % chi_squared)
    print('Reduced Chi Squared: %f' % reduced_chi_squared)

    # Create plot of data and fit
    matplotlib_errorbar(voltages, currents, fmt='g.', ecolor='black', markersize=4,
                        label='Collected Data', xerr=sigma_V, yerr=errors)
    matplotlib_plot(fit_V, fit_I, linestyle='--', c='red', linewidth=2, label='Fitted Model',)
    xlim(min(voltages), max(voltages))
    ylim(min(currents), max(currents))
    xlabel('Voltage (V)')
    ylabel('Current (A)')
    legend()

    # Show the plot if desired
    if open_plot:
        maptlotlib_show()

    # Save to output filename if given
    if output_filename:
        savefig(output_filename)
