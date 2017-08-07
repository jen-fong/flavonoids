import pandas as pd
import cufflinks as cf
import re
from filesys import Output
import experiment_variables
import graph


def get_csvs(month, wavelength, date='', data_folder=''):
    csv_adapter = Output()
    return csv_adapter \
           .get_path(month, wavelength, date, data_folder) \
           .find_all_csv()


def convert_data(month, wavelength, date=None):
    csv_adapter = Output()
    csvs = get_csvs(month, wavelength, data_folder='raw')

    for csv in csvs:
        df1 = pd.read_csv(str(csv))
        current_headers = df1.columns.values.tolist()

        # match all columns other than Sample1.
        # They are repeating columns with the wavelength and as such, useless
        # We need to delete it
        repeated_wavelength_columns = [h for h in current_headers if re.match('Sample[2-9]|Sample10', h)]
        df1 = df1.drop(repeated_wavelength_columns, axis=1)
        # Now we no longer need the Sample + unnamed column names
        # Instead we just reset the header to be the first row of the csv
        # and start the dataframe at row 1
        change_header = df1.iloc[0]
        df1 = df1[1:]
        df1 = df1.rename(columns=change_header)

        # Now remove all the rows after the last wavelength
        # Cary eclipse marks that row as the name of the first sample
        # In our case, it will always be Sample1
        # Then we remove the last row because it will just be Sample1
        wavelength_end = df1.loc[df1['Wavelength (nm)']=='Sample1'].index[0]
        df1 = df1[:wavelength_end]
        df1 = df1[:-1]
        df1 = df1.dropna(axis=1, how='all')
        df1 = df1.apply(pd.to_numeric, errors='ignore')
        # Finally, update all the headers so they do not just say intensity

        updated_headers = experiment_variables.get_header(wavelength, csv.stem)

        df1.columns = updated_headers
        df1 = df1.apply(pd.to_numeric, errors='ignore')
        buffer_control = df1['buffer control']
        buffer_exp = df1['buffer experiment']
        df1[updated_headers[1::2]] = df1[updated_headers[1::2]].apply(lambda x: x - buffer_control)
        df1[updated_headers[2::2]] = df1[updated_headers[2::2]].apply(lambda x: x - buffer_exp)

        df1 = df1.set_index('wavelength')

        date = csv.parts[len(csv.parents) - 2]

        print('Doing calculations for {} {}'.format(date, csv.name))
        Output() \
        .get_path(month, wavelength, date, 'processed') \
        .output_csv(df1, csv.name)


def create_line_graph(month, wavelength, date):
    cf.go_offline()
    csvs = get_csvs(month, wavelength, date, 'processed') \

    for csv in csvs:
        fig = graph.line_graph(csv, wavelength)
    
        filename = '{}.html'.format(csv.stem)
        date = csv.parts[len(csv.parents) - 2]

        print('Creating graph for {} {}'.format(date, filename))

        Output() \
        .get_path(month, wavelength, date, 'graphs') \
        .output_html(fig, filename)


def find_percent_difference(month, wavelength, date=None):
    csvs = get_csvs(month, wavelength, date,'processed')
    cf.go_offline()
    emit_data = []

    for csv in csvs:
        headers = experiment_variables.get_header(wavelength, csv.stem)
        df1 = pd.read_csv(
            str(csv),
            names=headers,
            index_col=0)
        df1 = df1[1:]
        df1 = df1.apply(pd.to_numeric, errors='ignore')
        
        differences = experiment_variables.determine_diff(wavelength, df1, csv.stem)

        print('Calculating % diff for {} at {} nm'.format(csv.stem, wavelength))

        flavonoid = csv.stem
        emit = {
            'flavonoid': csv.stem,
            'control': differences['control'],
            'experiment': differences['experiment'],
            'percent difference': differences['percent']
        }
        emit_data.append(emit)

    df2 = pd.DataFrame(emit_data, columns=['flavonoid', 'control', 'experiment', 'percent difference'])
    bar_graph = graph.bar_graph(df2)
    df2 = df2.set_index('flavonoid')

    csv_file = '{}.csv'.format(wavelength)
    graph_file = '{}.html'.format(wavelength)

    print('Creating bar graph...')
    analysis_path = Output() \
    .get_path(month, wavelength, 'difference', 'analysis') \
    .output_csv(df2, csv_file) \
    .output_html(bar_graph, graph_file)
