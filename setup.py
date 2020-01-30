import setuptools

REQUIREMENTS = [line for line in open('requirements.txt').read().split('\n') if line != '']

VERSION = '0.1.0'
AUTHOR = 'Igor Dias'
EMAIL = 'igorhenriquedias94@gmail.com'

setuptools.setup(
    name='sensecam_control',
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    license='MIT',
    description='Implementation of python functions for control and configuration of Axis cameras using Vapix/Onvif.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/smartsenselab/sensecam-control",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['ONVIF', 'vapix', 'camera'],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
)
