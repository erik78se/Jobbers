import setuptools

setuptools.setup(
    name='Jobbers',
    version='0.4dev',
    install_requires=['jinja2','inquirer','Click', 'confuse'],
    packages=setuptools.find_packages(),
    license='GPLv3',
    long_description=open('README.md').read(),
#     scripts=['bin/jobber'],
    entry_points={
        'console_scripts': [
            'abaqus-jobber=jobbers.abaqus.controller:cli',
            'femfat-jobber=jobbers.femfat.controller:cli',
            'tensor-jobber=jobbers.tensorflow.controller:cli',
        ],
    },
    include_package_data = True
)
