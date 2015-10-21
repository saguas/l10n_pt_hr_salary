# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='l10n_pt_hr_salary',
    version=version,
    description='Make salary for portugal',
    author='Luis Fernandes',
    author_email='luisfmfernandes@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
