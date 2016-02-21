"""
Reads in data analysis files from labview for diode characterization
"""

from argparse import ArgumentParser
from csv import reader

# Header text for labview files. Lines before and including a line with this text will be ignored
LABVIEW_HEADER_END_TEXT = '***End_of_Header***'

# Number of headers to ignore
LABVIEW_NUM_HEADERS = 2

def get_data(data_filename):
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

    # Return values, skipping any blank elements
    return [line for line in csv_reader if line]

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
