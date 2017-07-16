#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().split('\n')

with open('requirements_dev.txt') as requirements_dev_file:
    test_requirements = requirements + \
        requirements_dev_file.read().split('\n')[1:]


test_requirements = [r for r in test_requirements if r]

setup(
    name='trackr',
    version='1.0.0',
    description="-",
    long_description=readme,
    author="Renato Pedigoni",
    author_email='renatopedigoni@gmail.com',
    url='https://github.com/rpedigoni/trackr',
    packages=[
        'trackr',
    ],
    package_dir={'trackr':
                 'trackr'},
    entry_points={
        'console_scripts': [
            'trackr=trackr.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='trackr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
