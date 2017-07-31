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