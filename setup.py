import setuptools

setuptools.setup(
    name='Jobber',
    version='0.1dev',
    install_requires=['jinja2','inquirer'],
    packages=setuptools.find_packages(),
    license='GPLv3',
    long_description=open('README.txt').read(),
    scripts=['bin/somescript'],
    include_package_data = True
)
