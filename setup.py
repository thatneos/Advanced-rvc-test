from setuptools import setup, find_packages

# Read the requirements.txt file
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='rvc',
    version='0.1',
    description='rvc package',
    author='RVC people',
    packages=find_packages(),
    install_requires=requirements,  # Use the list of requirements here
)
