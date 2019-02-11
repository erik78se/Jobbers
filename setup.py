import setuptools

setuptools.setup(
    name='Jobber',
    version='0.1dev',
    install_requires=['jinja2','inquirer'],
    packages=setuptools.find_packages(),
    license='GPLv3',
    long_description=open('README.txt').read(),
#     scripts=['bin/jobber'],
    entry_points={
        'console_scripts': [
            'jobber=jobbers.jobber:process',
        ],
    },
    include_package_data = True
)
