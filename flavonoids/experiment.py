import pandas as pd
import cufflinks as cf
import re
from filesys import Output
import experiment_variables
import graph
import numpy as np


def get_csvs(wavelength=None, path_arr=[]):
    csv_adapter = Output()
    return csv_adapter \
           .make_path(path_arr) \
           .find_all_csv(wavelength)


def convert_data(month, wavelength, date=None):
    csv_adapter = Output()
    csvs = get_csvs(path_arr=['raw', month, wavelength])

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
    csvs = get_csvs(path_arr=['processed', month, wavelength, date])

    for csv in csvs:
        fig = graph.line_graph(csv, wavelength)
    
        filename = '{}.html'.format(csv.stem)
        date = csv.parts[len(csv.parents) - 2]

        print('Creating graph for {} {}'.format(date, filename))

        Output() \
        .get_path(month, wavelength, date, 'graphs') \
        .output_html(fig, filename)


def find_percent_decrease(experiment, month, wavelength, date=None):
    csvs = get_csvs(path_arr=['processed', month, wavelength, date])
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

        decreases = experiment_variables.determine_decrease(wavelength, df1, csv.stem)

        print('Calculating % diff for {} at {} nm'.format(csv.stem, wavelength))

        flavonoid = csv.stem
        emit = {
            'flavonoid': csv.stem,
            'control': decreases['control'],
            'experiment': decreases['experiment'],
            'percent decrease': decreases['percent']
        }
        emit_data.append(emit)

    df2 = pd.DataFrame(emit_data, columns=['flavonoid', 'control', 'experiment', 'percent decrease'])
    control_experiment = graph.graph(df2,
                                     kind='bar',
                                     barmode='group',
                                     x='flavonoid',
                                     y=['control', 'experiment'],
                                     yTitle='%',
                                     xTitle='Flavanoid',
                                     title= '% Decrease',
                                     asFigure=True)
    percent_dec_graph = graph.graph(df2,
                                    kind='bar',
                                    barmode='group',
                                    x='flavonoid',
                                    y='percent decrease',
                                    yTitle='%',
                                    xTitle='Flavanoid',
                                    title= '% Decrease',
                                    asFigure=True)
    df2 = df2.set_index('flavonoid')

    csv_file = '{}.csv'.format(wavelength)
    control_exp_html = 'control_exp_{}.html'.format(wavelength)
    percent_dec_html = 'precent_decrease_{}.html'.format(wavelength)

    print('Creating bar graph...')

    analysis_path = Output() \
    .make_path(['analysis', 'decrease', experiment]) \
    .output_csv(df2, csv_file) \
    .output_html(control_experiment, control_exp_html) \
    .output_html(percent_dec_graph, percent_dec_html)


def create_average(wavelength):
    csvs = get_csvs(wavelength, ['analysis', 'decrease'])
    cf.go_offline()

    all_flav_df = None
    for csv in csvs:
        headers = experiment_variables.get_header()
        df = pd.read_csv(
            str(csv),
            names=headers,
            index_col=0)
        df = df[1:]
        df = df.apply(pd.to_numeric, errors='ignore')

        current_headers = df.columns.values.tolist()

        columns_to_drop = ['control', 'experiment']

        df = df.drop(columns_to_drop, axis=1)

        if all_flav_df is None:
            all_flav_df = df
            continue

        all_flav_df = pd.merge(all_flav_df,
                               df, left_index=True,
                               right_index=True,
                               how='left')

    new_column_names = ['Experiment 1', 'Experiment 2', 'Experiment 3']
    all_flav_df.columns = new_column_names
    all_flav_df['average'] = all_flav_df.mean(axis=1)


    column_details = experiment_variables.get_column_details()
    ordered_column_details = []
    grouped_colors = []
    for k, v in column_details.items():
        ordered_column_details += v['names']
        # for name in v['names']:
        #     grouped_colors.append(v['color'])

    all_flav_df = all_flav_df.reindex(ordered_column_details)
    all_flav_df = all_flav_df.reset_index()

    avg_graph = graph.graph(all_flav_df,
                            kind='bar',
                            barmode='group',
                            x='flavonoid',
                            y='average',
                            yTitle='Average',
                            xTitle='Flavonoid',
                            title= 'Average % Decrease',
                            colors=['#3E6FB0'],
                            theme='white',
                            asFigure=True)

    all_with_avg_graph = graph.graph(all_flav_df,
                                     kind='bar',
                                     x='flavonoid',
                                     yTitle='Average',
                                     xTitle='Flavonoid',
                                     title='% Decrease from all Experiments',
                                     theme='space',
                                     asFigure=True)

    csv_file = 'average_{}.csv'.format(wavelength)
    avg_graph_file = 'average_{}.html'.format(wavelength)
    all_with_avg_file = 'all_with_avg_{}.html'.format(wavelength)

    print('creating bar graph for average for {}'.format(wavelength))
    analysis_path = Output() \
    .make_path(['analysis', 'average']) \
    .output_csv(all_flav_df, csv_file) \
    .output_html(avg_graph, avg_graph_file) \
    .output_html(all_with_avg_graph, all_with_avg_file)
