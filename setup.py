import codecs
import os
import re

from setuptools import find_packages, setup

project_root = os.path.dirname(os.path.abspath(__file__))
with codecs.open(
    os.path.join(project_root, "ntpc_tad_bot", "__init__.py"), "r", "latin1"
) as fp:
    try:
        version = re.findall(r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

install_requires = [
    "requests==2.27.1",
    "selenium==4.2.0",
]

dev_require = ["black==19.10b0", "pylint==2.5.0", "wheel==0.34.2"]

setup(
    name="ntpc_tad_bot",
    version=version,
    author="Chuang Double",
    author_email="ethan9141@gmail.com",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=install_requires,
    extras_require={"dev": dev_require},
    entry_points={"console_scripts": ["ntpc_tad_bot=ntpc_tad_bot.__main__:main"]},
)
