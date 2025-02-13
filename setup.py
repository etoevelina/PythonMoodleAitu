from setuptools import setup, find_packages

setup(
    name="myApp",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flet",
    ],
    entry_points={
        "console_scripts": [
            "myApp = myApp.main:main",
        ]
    },
)