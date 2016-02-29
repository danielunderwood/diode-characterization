"""
Reads in data analysis files from labview for diode characterization
"""

from argparse import ArgumentParser
from sys import version_info
from csv import reader
from collections import defaultdict

# Header text for labview files. Lines before and including a line with this text will be ignored
LABVIEW_HEADER_END_TEXT = '***End_of_Header***'

# Number of headers to ignore
LABVIEW_NUM_HEADERS = 2

# Dictionary for data rows
DATA_COL_KEYS = {'index': 0, 'out_voltage': 1, 'resistor1_voltage': 2, 'dut_voltage': 2}

def get_data(data_filename):
    """
    Gets the data from data_filename

    @param data_filename: Filename to parse data from
    @return Data from data_filename in a dictionary
    """
    with open(data_filename, 'r') as data_file:
        # Get actual csv output from file
        headers_found = 0
        csv_content = []
        for line in data_file:
            if LABVIEW_NUM_HEADERS > headers_found:
                if LABVIEW_HEADER_END_TEXT in line:
                    headers_found += 1
            else:
                csv_content.append(line)

    csv_reader = reader(csv_content, delimiter=',', quotechar="'")

    # Skip header line
    # Check version_info to make appropriate call for python 2 vs 3
    if version_info > (3,):
        csv_reader.__next__()
    else:
        csv_reader.next()

    # Build return dictionary
    ret = defaultdict(list)
    for line in csv_reader:
        # Skip line if empty
        if not line:
            continue

        for key, col in DATA_COL_KEYS.items():
            ret[key].append(float(line[col]))

        ret['filename'].append(data_filename)

    return ret

# If file is executed, get the data and print from filename argument
if __name__ == '__main__':

    # Set up parser
    parser = ArgumentParser(description='Load and print data file for diode characterization')
    parser.add_argument('filename', metavar='FILENAME', type=str)

    # Get filename from parser
    filename = parser.parse_args().filename

    # Load data from file
    data = get_data(filename)

    # Print data
    print(data)
