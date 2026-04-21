
import sys

from setuptools import setup

install_requires = {9: ["numpy==1.23.*", "pyparsing==3.1.*"],
                   11: ["numpy==1.23.*", "pyparsing==3.1.*"]}

setup(
name='dbcompound',
version = '1.0.0',
author='Evgenii Nekhoroshev',
author_email='evgnekhoroshev@gmail.com',
description='A Python package for working with the COMPOUND databases of FactSage software',
packages=['dbcompound'],
package_dir={'dbcompound': 'src'},
install_requires=install_requires.get(sys.version_info.minor)
)
