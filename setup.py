from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="rasterio_code_analyzer",
    version="1.0.0",
    description="Rasterio code analyzer",
    long_description=long_description,
    classifiers=[],
    keywords="",
    author=u"Sean Gillies",
    author_email="sean.gillies@gmail.com",
    url="https://github.com/sgillies/rasterio-code-analyzer",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    extras_require={"test": ["pytest"]},
)
