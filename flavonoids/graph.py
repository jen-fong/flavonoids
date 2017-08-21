from filesys import Output
import cufflinks as cf
import pandas as pd
import experiment_variables


def line_graph(csv, wavelength):
    headers = experiment_variables.get_header(wavelength, csv.stem)
    df1 = pd.read_csv(
            str(csv),
            names=headers,
            index_col=0)
        # Need to check if I need this
    df1 = df1[1:]

    fig = graph(df1,
                kind = 'lines',
                size=5, asFigure=True,
                xTitle = 'Wavelength (nm)',
                yTitle = 'Intensity (A.U)')

    return fig


def graph(df, **kwargs):
    fig = df.iplot(**kwargs)

    return fig


def percent_decrease(x, y):
    return ((x - y) * 100) / x
