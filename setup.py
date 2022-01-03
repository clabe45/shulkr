from glob import glob
import os.path
from setuptools import find_packages, setup
from typing import List


def package_files(directory: str) -> List[str]:
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


script_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(script_dir, 'README.md'), 'r') as f:
	README = f.read()

classifiers = [
	'Development Status :: 2 - Pre-Alpha',
	'Environment :: Console',
	'Intended Audience :: Developers',
	'Intended Audience :: Science/Research',
	'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
	'Operating System :: OS Independent',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3',
	'Topic :: Games/Entertainment',
	'Topic :: Scientific/Engineering',
	'Topic :: Software Development :: Version Control :: Git',
	'Topic :: Utilities'
]

setup(
	name='shulkr',
	version='0.3.3',
	description='Decompile multiple versions of Minecraft with a single command (for research)',
	long_description=README,
	long_description_content_type='text/markdown',
	url='https://github.com/clabe45/shulkr',
	author='Caleb Sacks',
	license='GPLv3',
	classifiers=classifiers,
    keywords=['minecraft', 'git', 'decompile', 'game'],
    packages=find_packages(exclude=['tests']),
    py_modules=['shulkr'],
	include_package_data=True,
	package_data={'': package_files('shulkr/DecompilerMC')},
	install_requires=['gitpython', 'javalang', 'unidiff', 'requests'],
	entry_points={
        'console_scripts': ['shulkr=shulkr.__main__:main']
    }
)