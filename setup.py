from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='gps_utils',  # Required
    version='0.0.1',  # Required
    description='Functions for retrieving and parsing gps data.',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/GraemeKnowles/gps_utils',  # Optional
    author='Graeme Knowles',  # Optional
    keywords='GPS, Almanac, Ephemeris',  # Optional
    packages=find_packages(),  # Required
    python_requires='>=3.5, <4',
    install_requires=['requests'],  # Optional
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/GraemeKnowles/gps_utils/issues',
        'Source': 'https://github.com/GraemeKnowles/gps_utils',
    },
)
