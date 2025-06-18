from setuptools import setup, find_packages

setup(
    name='pydantic_rest_client',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'aiohttp>=3.8.0',
        'pydantic>=2.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    python_requires='>=3.8',
    author='Damian Sop',
    author_email='damian.sop.official@gmail.com',
    license="MIT",
    description='RESTful client with pydantic validation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DamianSop/pydantic_rest_client',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: HTTP Clients',
    ],
    keywords='rest api client pydantic validation async',
)
