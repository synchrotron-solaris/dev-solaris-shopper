from setuptools import find_packages, setup

from shopper_ds.version import __version__, licence
from shopper_ds import __doc__, __author__, __author_email__

setup(
    name="tangods-shopper",
    author=__author__,
    author_email=__author_email__,
    version=__version__,
    license=licence,
    description="Tango DeviceServer for the shopper device (integrated shutter "
                "and stopper).",
    long_description=__doc__,
    url="https://github.com/synchrotron-solaris/dev-solaris-shopper.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["setuptools"],
    entry_points={
        "console_scripts": ["Shopper = "
                            "shopper_ds.shopper:run"]}
)
