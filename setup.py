import os
from setuptools import setup, find_packages

long_description = (
    open('README.txt').read()
    + '\n' +
    open('CHANGES.txt').read())


setup(
    name='babel-obviel',
    version='0.6',
    description='Obviel Template message extractor for Babel',
    long_description=long_description,
    author='Obviel Developers',
    author_email='obviel@googlegroups.com',
    packages=['babelobviel'],
    include_package_data = True,
    zip_safe=False,
    license='BSD',
    install_requires=[
        'lxml',
    ],
    extras_require=dict(
        test=['pytest >= 2.0'],
        ),
    entry_points="""
    [babel.extractors]
    obvt = babelobviel.obvt:extractor
    obvt_html = babelobviel.obvt:html_extractor
    """,
    )
