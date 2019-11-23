from setuptools import setup, find_packages

setup(
    name='myfoo',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'PyYAML>=5.1',
        'requests',
        'openpyxl',
    ]
)


# install poppler w/ conda
#    conda install -c conda-forge poppler
# or homebrew
#    brew install poppler
