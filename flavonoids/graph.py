from filesys import Output
import cufflinks as cf
import pandas as pd


def create():
    cf.go_offline()
    csv_adapter = Output()
    csvs = csv_adapter.get_path('2014-04', '570', '160423', 'analysis').find_all_csv()

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
        Output().get_path('2014-04', '570', '160423', 'graphs').output_html(fig, filename)
