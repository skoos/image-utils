from setuptools import setup, find_packages

with open('requirements.txt', 'r') as reqfile:
    setup(
        name='imageutils',
        version='0.1',
        package_dir={'':'src'},
        packages=find_packages('src'),
        install_requires=reqfile.readlines()
    )
