import setuptools

setuptools.setup(
    name='Jobbers',
    version='0.4.1',
    install_requires=['jinja2', 'inquirer', 'Click', 'confuse'],
    packages=setuptools.find_packages(),
    license='GPLv3',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': [
            'abaqus-jobber=jobbers.abaqus.controller:cli',
            'femfat-jobber=jobbers.femfat.controller:cli',
            'tensor-jobber=jobbers.tensorflow.controller:cli',
        ],
    },
    include_package_data=True
)
