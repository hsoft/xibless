from setuptools import setup
from xibless import __version__

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Environment :: Console',
    'License :: OSI Approved :: BSD License',
    'Operating System :: MacOS :: MacOS X',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Objective C',
    'Topic :: Software Development :: Code Generators',
]

LONG_DESC = open('README', 'rt').read() + '\n\n' + open('CHANGES', 'rt').read()

setup(
    name='xibless',
    version=__version__,
    author='Virgil Dupras',
    author_email='hsoft@hardcoded.net',
    packages=['xibless'],
    url='http://hg.hardcoded.net/xibless/',
    license='BSD',
    description="Generate Objective-C code that builds Cocoa UIs. Replaces XCode's XIBs",
    long_description=LONG_DESC,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'xibless = xibless:main',
        ],
    },
    command_options={
       'build_sphinx': {
           'version': ('setup.py', __version__),
           'release': ('setup.py', __version__)}
    },
)