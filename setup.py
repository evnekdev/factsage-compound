
import sys

from setuptools import setup

install_requires = {9: ["numpy==1.23.*", "pyparsing==3.1.*"],
                   11: ["numpy==1.23.*", "pyparsing==3.1.*"]}

setup(
name='factsage-compound',
version = '1.0.0',
author='Evgenii Nekhoroshev',
author_email='evgnekhoroshev@gmail.com',
description='A Python package for working with the COMPOUND databases of FactSage software',
packages=['factsage_compound'],
package_dir={'factsage_compound': 'src/factsage_compound'},
install_requires=["numpy>=1.23", "pyparsing>=3.1"]
)
