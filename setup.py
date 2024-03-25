from setuptools import setup, find_packages

setup(
    name='pydantic_rest_client',
    version='1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'aiohttp',
        'pydantic',
    ],
    author='Damian Sop',
    author_email='damian.sop.official@gmail.com',
    license="MIT",
    description='RESTful client with pydantic validation',
    url='https://github.com/DamianSop/pydantic_rest_client',
)
