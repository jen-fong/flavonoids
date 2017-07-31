from filesys import Output
import cufflinks as cf
import pandas as pd
import numpy as np

def line_graph(csv):
    df1 = pd.read_csv(
            str(csv),
            names=['buffer control',
                   'buffer experiment',
                   'liposomes control',
                   'liposomes + {}'.format(csv.stem),
                   'cyt c control',
                   'cyt c experiment',
                   'amplex red control',
                   'amplex red experiment',
                   'H2O2 control',
                   'H2O2 experiment'],
            index_col=0)
        # Need to check if I need this
    df1 = df1[1:]

    fig = df1.iplot(kind = 'lines',
                    size=5, asFigure=True,
                    xTitle = 'Wavelength (nm)',
                    yTitle = 'Intensity (A.U)')

    return fig


def bar_graph(csv):
    # TODO
    # Move all headeers into constants
    # Read it all in a condfig
    # store all arrays in that config so that we can
    # read all headers from there
    # Everything else should be the same
    pass


def percent_diff(x, y):
    return ((x - y) * 100) / x


def create(month, wavelength, date):
    cf.go_offline()
    csv_adapter = Output()
    csvs = csv_adapter \
           .get_path(month, wavelength, date, 'processed') \
           .find_all_csv()

    for csv in csvs:
        fig = line_graph(csv)
    
        filename = '{}.html'.format(csv.stem)
        date = csv.parts[len(csv.parents) - 2]

        print('Creating graph for {} {}'.format(date, filename))
        data = fig.get_data()

        Output() \
        .get_path(month, wavelength, date, 'graphs') \
        .output_html(fig, filename)


def get_value(month, wavelength, date=None):
    # loop over all the files and grab the values for last two
    # columns for all flavs
    # create a new dataframe from this and save
    # Plot as bar graph
    # we need to plot % difference and % inhibition!
    # Just open the file like create and just return the csv from loop
    cf.go_offline()
    csv_adapter = Output()
    csvs = csv_adapter \
           .get_path(month, wavelength, date, 'processed') \
           .find_all_csv()
    emit_data = []

    for csv in csvs:
        df1 = pd.read_csv(
            str(csv),
            names=['wavelength',
                   'buffer control',
                   'buffer experiment',
                   'liposomes control',
                   'liposomes + {}'.format(csv.stem),
                   'cyt c control',
                   'cyt c experiment',
                   'amplex red control',
                   'amplex red experiment',
                   'H2O2 control',
                   'H2O2 experiment'],
            index_col=0)
        df1 = df1[1:]
        df1 = df1.apply(pd.to_numeric, errors='ignore')
        
        h2o2_control = df1.loc['584.9199829', 'H2O2 control']
        h2o2_experiment = df1.loc['584.9199829', 'H2O2 experiment']
        ared_control = df1.loc['584.9199829', 'amplex red control']
        ared_experiment = df1.loc['584.9199829', 'amplex red experiment']

        control_diff = h2o2_control - ared_control
        experiment_diff = h2o2_experiment - ared_experiment
        flavonoid = csv.stem
        emit = {
            'flavonoid': csv.stem,
            'control': control_diff,
            'experiment': experiment_diff,
            'percent difference': percent_diff(control_diff, experiment_diff)
        }
        emit_data.append(emit)

    df2 = pd.DataFrame(emit_data)
    df2 = df2.set_index('flavonoid')

    csv_file = '{}.csv'.format(wavelength)
    graph_file = '{}.html'.format(wavelength)

    Output() \
    .get_path(month, wavelength, 'difference', 'analysis') \
    .output_csv(df2, csv_file)
    # .output_html(df2, graph_file)
    # need to save data here