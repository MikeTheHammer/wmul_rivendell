"""
@Author = 'Michael Stanley'

This is the setup file for the package.

============ Change Log ============
2020-Jul-25 = Added GPL notice.

2020-Jun-25 = Created.

============ License ============
Copyright (C) 2020 Michael Stanley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from setuptools import setup, find_packages

setup(
    name='wmul_rivendell',
    version='0.11.0',
    license='GPLv2',
    description='Various scripts to help use Rivendell Radio Automation 3.4.1+',

    author='Michael Stanley',
    author_email='stanley50@marshall.edu',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['wmul_logger>=0.5.0', 'wmul_emailer>=0.3.0', 'click', "mysql-connector-python",
                      "cachetools", "dataclasses;python_version < '3.7.0'",
                      "protobuf<=3.19.4;python_version < '3.7.0'", "protobuf>=3.19.0;python_version > '3.7.0'"],
    tests_require=["pytest", "pyfakefs", "pytest-mock", "wmul_test_utils>=0.1.0"],

    entry_points='''
        [console_scripts]
        wmul_rivendell=wmul_rivendell.cli:wmul_rivendell_cli
    '''
)
