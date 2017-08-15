import argparse
import sys
import experiment


def init_parser():
    parser = argparse.ArgumentParser(
        description='Processes csv data for research data \
                     and creates plotly graphs from the data')

    parser.add_argument('-m', '--month',
                        help='Enter a year and month in format yyyy-mm')
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
    parser.add_argument('--decrease',
                        action='store_true',
                        help='Processes the percent diff for each compound')
    parser.add_argument('--avg',
                        action='store_true',
                        help='Creates avg of all experiment data')
    return parser

def init_convert(parser):
    args = parser.parse_args()
    month = args.month
    nm = args.wavelength
    date = args.date

    if args.convert is None and args.graph is None:
        print('Please choose an option')
        sys.exit(1)

    if args.convert and month:
        experiment.convert_data(month, nm, date)

    # give ability to convert to csv and graph in one step
    if args.graph and month:
        experiment.create_line_graph(month, nm, date)

    if args.decrease and month:
        experiment.find_percent_decrease(month, nm)

    if args.avg:
        experiment.create_average(nm)

if __name__ == "__main__":
    init_convert(init_parser())