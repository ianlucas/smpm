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
