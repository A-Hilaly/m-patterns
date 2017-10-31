from setuptools import setup, find_packages, Command


setup(
    name='madpatterns.py',
    version='0.0.1',
    description='pattern validator',
    author='M.A.H',
    author_email='',
    packages=find_packages(exclude=('docs', '.circleci')),
)
