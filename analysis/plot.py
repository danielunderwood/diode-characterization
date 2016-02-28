import seaborn
import pandas
from argparse import ArgumentParser
from data import get_data

def plot_data(currents, voltages):
    """
    Plots the IV curve for one plot

    @param currents: List of currents to plot
    @param voltages: List of voltages to plot
    """

    # Gather data into pandas dataframe
    data_frame = pandas.DataFrame()

    data_frame['Voltage'] = voltages
    data_frame['Current'] = currents

    return seaborn.lmplot(x='Voltage', y='Current', data=data_frame, fit_reg=False)

if __name__ == '__main__':

    # Set up parset to get filename
    parser = ArgumentParser(description='Load and plot data file for diode characterization')
    parser.add_argument('filename', metavar='FILENAME', type=str)
    parser.add_argument('resistance', metavar='RESISTANCE', type=float)

    filename = parser.parse_args().filename
    resistance = parser.parse_args().resistance

    # Load data from file
    data = get_data(filename)

    # Calculate currents
    currents = [voltage / resistance for voltage in data['resistor1_voltage']]
    voltages = data['dut_voltage']

    plot = plot_data(currents, voltages)
    plot.savefig(filename + '_plot.pdf')

