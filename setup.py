from setuptools import setup, find_packages

setup(
    name="myserver",
    version="0.1",
    packages=find_packages(),  # will include both myserver/ and computer_control_project/
    install_requires=[],       # or read from requirements.txt, up to you
)
