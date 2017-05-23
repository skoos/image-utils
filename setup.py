from setuptools import setup, find_packages

with open('requirements.txt', 'r') as reqfile:
    setup(
        name='imageutils',
        version='0.1',
        description='Small utility library for image loading/manipulation',
        url='http://github.com/skoos/image-utils',
        package_dir={'':'src'},
        packages=find_packages('src'),
        install_requires=reqfile.readlines()
    )
