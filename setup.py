from setuptools import setup

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
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
    version='0.1.0',
    author='Virgil Dupras',
    author_email='hsoft@hardcoded.net',
    packages=['xibless'],
    scripts=[],
    install_requires=[],
    url='http://hg.hardcoded.net/xibless/',
    license='BSD',
    description="Generate Objective-C code that builds Cocoa UIs. Replaces XCode's XIBs",
    long_description=LONG_DESC,
    classifiers=CLASSIFIERS,
    entry_points = {
        'console_scripts': [
            'xibless = xibless:main',
        ],
    },
)