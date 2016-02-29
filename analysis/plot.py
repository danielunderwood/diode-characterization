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

    return seaborn.lmplot(x='Voltage', y='Current', col='File', data=data_frame, fit_reg=False, col_wrap=4)

if __name__ == '__main__':

    # Set up parset to get filename
    parser = ArgumentParser(description='Load and plot data file for diode characterization')
    parser.add_argument('resistance', metavar='RESISTANCE', type=float)
    parser.add_argument('filenames', nargs='*')

    filenames_arg = parser.parse_args().filenames
    resistance = parser.parse_args().resistance

    # Load data from file
    currents = []
    voltages = []
    filenames = []
    for filename in filenames_arg:
        data = get_data(filename)
        currents += [voltage / resistance for voltage in data['resistor1_voltage']]
        voltages += [datum for datum in data['dut_voltage']]

        # Add filename for each point in data
        filenames += [filename for datum in data['index']]

    plot = plot_data(currents, voltages, filenames)
    seaborn.plt.show()
    plot.savefig(filename + '_plot.pdf')
