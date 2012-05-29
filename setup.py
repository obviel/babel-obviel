import os
from setuptools import setup, find_packages

setup(
    name='babel-obviel',
    version='0.5dev',
    description='Obviel Template message extractor for Babel',
    long_description='',
    author='Obviel Developers',
    author_email='obviel@googlegroups.com',
    packages=['babelobviel'],
    include_package_data = True,
    zip_safe=False,
    license='BSD',
    install_requires=[
        'lxml',
        'Babel',
    ],
    extras_require=dict(
        test=['pytest >= 2.0'],
        ),
    entry_points="""
""",
    )
