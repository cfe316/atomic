import os

extension_modules = {}
directory = 'src/xxdata_11'
sources = ['xxdata_11.for', 'xxrptn.for', 'i4unit.for',
    'i4fctn.for', 'xxword.for', 'xxcase.for', 'xfelem.for', 'xxslen.for',
     '../xxdata_11.pyf', '../helper_functions.for']
extension_modules['_xxdata_11'] = dict(sources=sources, directory=directory)


directory = 'src/xxdata_15'
sources = ['xxdata_15.for', 'xxrptn.for', 'xxmkrp.for', 'i4unit.for',
    'i4fctn.for', 'r8fctn.for', 'xxhkey.for', 'xxword.for', 'xxcase.for',
    'i4eiz0.for', 'xfelem.for', 'xxslen.for',
     '../xxdata_15.pyf', '../helper_functions.for']
extension_modules['_xxdata_15'] = dict(sources=sources, directory=directory)


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('atomic', parent_package, top_path)


    for module, values in extension_modules.iteritems():
        directory = values['directory']
        sources = values['sources']
        sources = [os.path.join(directory, i) for i in sources]

        config.add_extension(module, sources)
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

