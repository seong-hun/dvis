import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dvis',
    version='0.0.0',
    url='https://github.com/seong-hun/dvis',
    author='Seong-hun Kim',
    author_email='kshoon92@gmail.com',
    description='Drone visualization toolbox',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    license_files=['LICENSE'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        'numpy',
        'matplotlib',
    ]
)
