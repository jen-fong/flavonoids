from filesys import Output
import cufflinks as cf
import pandas as pd


def create(month, wavelength, date):
    cf.go_offline()
    csv_adapter = Output()
    csvs = csv_adapter \
           .get_path(month, wavelength, date, 'analysis') \
           .find_all_csv()

    for csv in csvs:
        df1 = pd.read_csv(str(csv),
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
        df1 = df1[1:]
    #     fig = df1.iplot(asFigure=True)

    #     plotly.offline.plot(fig,filename="example.html")
        fig = df1.iplot(kind = 'lines', mode = 'markers',
                        size=5, asFigure=True,
                        xTitle = 'Wavelength (nm)',
                        yTitle = 'Intensity (A.U)')
    
        filename = '{}.html'.format(csv.stem)
        date = csv.parts[len(csv.parents) - 2]

        print('Creating graph for {} {}'.format(date, filename))
        Output() \
        .get_path(month, wavelength, date, 'graphs') \
        .output_html(fig, filename)
