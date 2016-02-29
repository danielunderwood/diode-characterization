import seaborn
import pandas
from argparse import ArgumentParser
from data import get_data

def plot_data(currents, voltages, filenames):
    """
    Plots the IV curve for one plot

    @param currents: Currents to plot
    @param voltages: Voltages to plot
    @param filenames: Filenames to plot
    @return Plot handle
    """

    # Gather data into pandas dataframe
    data_frame = pandas.DataFrame({'Current': currents, 'Voltage': voltages, 'File': filenames})

    return seaborn.lmplot(x='Voltage', y='Current', col='File', data=data_frame, fit_reg=False)

if __name__ == '__main__':

    # Set up parset to get filename
    parser = ArgumentParser(description='Load and plot data file for diode characterization')
    parser.add_argument('filename', metavar='FILENAME', type=str)
    parser.add_argument('resistance', metavar='RESISTANCE', type=float)

    filename = parser.parse_args().filename
    resistance = parser.parse_args().resistance

    # Load data from file
    data = get_data(filename)

    # Build data
    currents = [voltage / resistance for voltage in data['resistor1_voltage']]
    voltages = data['dut_voltage']
    filenames = data['filename']

    plot = plot_data(currents, voltages, filenames)
    seaborn.plt.show()
    plot.savefig(filename + '_plot.pdf')

