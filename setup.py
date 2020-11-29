from setuptools import setup

setup(
    name='error_analysis',
    version='0.0.1',
    packages=['error_analysis'],
    install_requires=[
        'numpy',
        'scipy',
        'sympy',
        'matplotlib',
        'varname'
    ],
    url='https://github.com/finnschwall/ErrorAnalysis',
    license='',
    author='finns',
    author_email='unjqc@student.kit.edu',
    description='Small library for easier propagation of uncertainty'
)
