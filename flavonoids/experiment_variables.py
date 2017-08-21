import graph


def get_header(wavelength='', flavanoid=''):
    if wavelength == '570':
        return ['wavelength',
               'buffer control',
               'buffer experiment',
               'liposomes control',
               'liposomes + {}'.format(flavanoid),
               'cyt c control',
               'cyt c experiment',
               'amplex red control',
               'amplex red experiment',
               'H2O2 control',
               'H2O2 experiment']
    if wavelength == '293':
        return ['wavelength',
               'buffer control',
               'buffer experiment',
               'cyt c control',
               'cyt c experiment',
               'liposomes control',
               'liposomes + {}'.format(flavanoid)]

    return ['flavonoid', 'control', 'experiment', 'percent decrease']


def determine_decrease(wavelength, df, flavanoid):
    point_570 = '584.9199829'
    point_293 = '347.07000730000004'
    if wavelength == '570':
        h2o2_control = df.loc[point_570, 'H2O2 control']
        h2o2_experiment = df.loc[point_570, 'H2O2 experiment']
        ared_control = df.loc[point_570, 'amplex red control']
        ared_experiment = df.loc[point_570, 'amplex red experiment']

        control_diff = h2o2_control - ared_control
        experiment_diff = h2o2_experiment - ared_experiment

        return {
            'control': control_diff,
            'experiment': experiment_diff,
            'percent': graph.percent_decrease(control_diff, experiment_diff)
        }

    if wavelength == '293':
        lip_flav = df.loc[point_293, 'liposomes + {}'.format(flavanoid)]
        lip_control = df.loc[point_293, 'liposomes control']
        print(graph.percent_decrease(lip_control, lip_flav))
        return {
            'control': lip_control,
            'experiment': lip_flav,
            'percent': graph.percent_decrease(lip_control, lip_flav)
        }


def get_column_details():
    return {
        "flavanones": {
            "names": ['flavanone', 'hesperetin', 'naringenin', 'naringin'],
            "color": 'blue'
        },
        "flavanols": {
            "names": ['catechin', 'epigallocatechin gallate'],
            "color": 'green'
        },
        "flavonols": {
            "names": ['fisetin', 'kaempferol', 'myricetin', 'rutin trihydrate'],
            "color": 'pink'
        },
        "flavones": {
            "names": ['baicalein', 'diosmin', 'flavone', 'luteolin'],
            "color": 'orange'
        },
        "isoflavones": {
            "names": ['biochanin a', 'daizden', 'genistein'],
            "color": 'yellow'
        },
        "flavanonols": {
            "names": ['taxifolin'],
            "color": 'red'
        }
    }
