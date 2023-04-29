# ---------------------------------------------------------------------------------------------
#  Copyright (c) Ian Lucas. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------------------------------------------

from setuptools import setup, find_packages

setup(
    name="smpm",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={"console_scripts": ["smpm = smpm.cli:main"]},
)
