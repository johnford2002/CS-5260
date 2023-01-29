from setuptools import setup

install_deps = []
with open('requirements.txt') as file:
   install_deps.extend([line for line in file])

setup(install_requires=install_deps)
