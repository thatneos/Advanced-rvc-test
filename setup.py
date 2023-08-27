from setuptools import setup, find_packages
import pkg_resources

# Read the requirements.txt file
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

path_to_json = pkg_resources.resource_filename('rvc', 'lib/uvr5_pack/lib_v5/modelparams/4band_v2.json')

setup(
    name='rvc',
    version='0.1',
    description='rvc package',
    author='RVC people',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
)
