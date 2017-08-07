import graph


def get_header(wavelength, flavanoid):
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


def determine_diff(wavelength, df, flavanoid):
    print(df)
    point_570 = '584.9199829'
    point_293 = '324.0'
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
            'percent': graph.percent_diff(control_diff, experiment_diff)
        }

    if wavelength == '293':
        lip_flav = df.loc[point_293, 'liposomes + {}'.format(flavanoid)]
        lip_control = df.loc[point_293, 'liposomes control']
        print(graph.percent_diff(lip_control, lip_flav))
        return {
            'control': lip_control,
            'experiment': lip_flav,
            'percent': graph.percent_diff(lip_control, lip_flav)
        }