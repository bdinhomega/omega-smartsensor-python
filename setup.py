import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='omegasensor',
    version='0.1',
    author="Binh Dinh",
    author_email="bdinh@omega.com",
    description="Omega Smartsensor Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdinhomega/omega-smartsensor-python",
    packages=setuptools.find_packages(),
    install_requires=['MinimalModbus', 'bitstruct'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )