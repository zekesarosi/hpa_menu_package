from setuptools import setup, find_packages


VERSION = '0.1.3'
DESCRIPTION = 'A python package intended for Hawaii Preparatory Academy'
LONG_DESCRIPTION = 'A package that uses requests and a data parsing function to pull menu data from Flik/Nutrislice backend API in order to make it' \
                   'easy to integrate with 3rd party applications. '

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="verysimplemodule",
    version=VERSION,
    author="Jason Dsouza",
    author_email="<youremail@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],  # add any additional packages that
    # needs to be installed along with the package'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)