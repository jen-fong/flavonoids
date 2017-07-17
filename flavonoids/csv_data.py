from pathlib import Path
import pandas as pd
import re


# These two classes are for file/folder manipulation of the csv data files
class Csvs:
    def __init__(self):
        self.path = Path('csv_data/')

    def get_path(self, month, wavelength, date, raw='raw'):
        # can takea direct path to the folder
        # should use this for the command line flags
        self.path = self.path / raw / month / wavelength / date
        
        return self

    def find_all_csv(self):
        return [f for f in self.path.glob('**/*') if f.is_file()] 

class Csv(Csvs):
    def output_csv(self,df, name):
        # Ensure all folders exist and if not, create them
        # Finally, save to csv
        self.path.mkdir(exist_ok=True, parents=True)
        file_name = self.path.joinpath(name)
        df.to_csv(file_name, sep=',')
        return file_name


def convert(month=None, wavelength=None, date=None):
    csv_adapter = Csv()
    csvs = csv_adapter.get_path('2014-04', '570', '160408').find_all_csv()

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

        # Finally, update all the headers so they do not just say intensity
        updated_headers = ['wavelength',
                           'buffer control',
                           'buffer experiment',
                           'liposomes control',
                           'liposomes + {}'.format(csv.stem),
                           'cyt c control',
                           'cyt c experiment',
                           'amplex red control',
                           'amplex red experiment',
                           'H2O2 control',
                           'H2O2 experiment']
        df1.columns = updated_headers

        df1 = df1.apply(pd.to_numeric, errors='ignore')
        buffer_control = df1['buffer control']
        buffer_exp = df1['buffer experiment']
        df1[updated_headers[3::2]] = df1[updated_headers[3::2]].apply(lambda x: x - buffer_control)
        df1[updated_headers[4::2]] = df1[updated_headers[4::2]].apply(lambda x: x - buffer_exp)

        Csv().get_path('2014-04', '570', '160408', 'analysis').output_csv(df1, csv.name)