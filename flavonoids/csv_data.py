import pandas as pd
import re
from filesys import Output
import header_variables


def convert(month, wavelength, date=None):
    csv_adapter = Output()
    csvs = csv_adapter.get_path(month, wavelength, date).find_all_csv()

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
        print(df1)
        updated_headers = header_variables.get_header(wavelength, csv.stem)
        print(updated_headers)
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