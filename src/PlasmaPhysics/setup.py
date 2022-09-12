# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:56:26 2022

@author: jeffrey bonde
"""

from setuptools import setup

from ._version import get_versions

vinfo = get_versions()

setup(
      python_requires='>='+vinfo["python"]
      )

del get_versions, vinfo