from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in complaints_management/__init__.py
from complaints_management import __version__ as version

setup(
	name="complaints_management",
	version=version,
	description="Lecico Complaints Management System",
	author="Josef Engelskirchen",
	author_email="josef.engelskirchen@outlook.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
