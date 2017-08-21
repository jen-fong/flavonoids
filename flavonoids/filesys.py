from pathlib import Path
import plotly

# These two classes are for file/folder manipulation of the csv data files
class Csvs:
    def __init__(self):
        self.path = Path('csv_data/')

    def get_main_path(self, folder):
        self.path = self.path / folder
        return self

    def make_path(self, path_arr=[]):
        for p in path_arr:
            if p is None:
                continue
            self.path = self.path / p

        return self

    def get_nested_path(self, month, wavelength, date):
        self.path = self.path / month / wavelength
        if date:
            self.path = self.path / date
        return self
    
    def get_path(self, month, wavelength, date, folder):
        # can takea direct path to the folder
        # should use this for the command line flags
        self.get_main_path(folder)
        self.get_nested_path(month, wavelength, date)
        return self

    def find_all_csv(self, wavelength=''):
        pattern = '**/*.csv'
        if wavelength:
            pattern = '**/*.csv'
        return [f for f in self.path.glob(pattern) if f.is_file()]


class Output(Csvs):
    def set_path (self, name):
        # Ensure all folders exist and if not, create them
        # Finally, save to csv
        self.path.mkdir(exist_ok=True, parents=True)
        return self.path.joinpath(name)

    def output_csv(self, df, name):
        filename = self.set_path(name)
        df.to_csv(filename, sep=',')
        return self

    def output_html(self, fig, name):
        # stringify the path for regular usage
        filename = str(self.set_path(name))
        plotly.offline.plot(fig,filename=filename, auto_open=False)
        return self
