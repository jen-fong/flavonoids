import argparse
import sys
import experiment


def init_parser():
    parser = argparse.ArgumentParser(
        description='Processes csv data for research data \
                     and creates plotly graphs from the data')

    parser.add_argument('-m', '--month',
                        help='Enter a year and month in format yyyy-mm',
                        required=True)
    parser.add_argument('-w', '--wavelength',
                        help='Enter the wavelength, 570 or 293',
                        choices=['570', '293'],
                        required=True)
    parser.add_argument('-d', '--date',
                        help='Enter a date in format yymmdd')
    parser.add_argument('--convert',
                        action='store_true',
                        help='convert raw csv data')
    parser.add_argument('--graph',
                        action='store_true',
                        help='Create graphs of data')
    parser.add_argument('--diff',
                        action='store_true',
                        help='Processes the percent diff for each compound')
    return parser

def init_convert(parser):
    args = parser.parse_args()
    month = args.month
    nm = args.wavelength
    date = args.date

    if args.convert is None and args.graph is None:
        print('Please choose convert or graph')
        sys.exit(1)

    if args.convert:
        experiment.convert_data(month, nm, date)

    # give ability to convert to csv and graph in one step
    if args.graph:
        experiment.create_line_graph(month, nm, date)

    if args.diff:
        experiment.find_percent_difference(month, nm)

if __name__ == "__main__":
    init_convert(init_parser())