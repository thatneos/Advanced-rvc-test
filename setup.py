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
    install_requires=requirements,
    package_data={
        'lib.uvr5_pack.lib_v5.modelparams': ['*.json']
    }
    
)
