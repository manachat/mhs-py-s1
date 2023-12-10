
from setuptools import setup, find_packages 

dependencies = [ 
    'click>=8.1.7', 
] 

setup( 
    name='hw1', 
    version='1.0.0', 
    description='hw1 lol', 
    packages=find_packages(), 
    install_requires=dependencies 
) 