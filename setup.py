from setuptools import setup
from setuptools import find_packages
import os

def find_data_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setup(
    name='TypingMusician',
    version='1.0',
    description="Simple, yet amazing rhythm game for all speed typists!",
    author="Adam Mikołajczyk",
    packages=find_packages(),
    install_requires=[
        'pygame',
        'librosa',
        'numpy'
    ],
    python_requires="~=3.5",
    package_data={
        '': ['*.csv'],
        '': ['README.md'],
        'fonts': ['*'],
        'graphics': find_data_files('graphics'),
        'songs': find_data_files('songs'),
        'sounds': ['*']
    },
    entry_points={
        'console_scripts': ['typing_musician = game:main_menu']
    }
)
