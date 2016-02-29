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
    parser.add_argument('--output', type=str)
    parser.add_argument('--open-plot', dest='plot', action='store_true')
    parser.add_argument('filenames', nargs='*')

    filenames_arg = parser.parse_args().filenames
    resistance = parser.parse_args().resistance
    output_file = parser.parse_args().output
    open_plot = parser.parse_args().plot

    # Load data from file
    currents = []
    voltages = []
    filenames = []
    for filename in filenames_arg:
        data = get_data(filename)
        currents += [voltage / resistance for voltage in data['resistor1_voltage']]
        voltages += [datum for datum in data['dut_voltage']]

        # Add filename for each point in data
        filenames += [filename for datum in data['dut_voltage']]

    plot = plot_data(currents, voltages, filenames)

    # Open the plot if flag is used
    if open_plot:
        seaborn.plt.show()

    # Save the figure if we have an output
    if output_file:
        plot.savefig(output_file)

