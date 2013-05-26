import pep438
from setuptools import setup, find_packages


setup(
    name=pep438.__title__,
    version=pep438.__version__,
    author=pep438.__author__,
    url="https://github.com/treyhunner/pep438",
    description="Check your requirements for proper PEP 438 usage.",
    long_description='\n\n'.join((
        open('README.rst').read(),
        open('CHANGES.rst').read(),
        open('CONTRIBUTING.rst').read(),
    )),
    license=open('LICENSE').read(),
    packages=find_packages(),
    py_modules=['pep438'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pep438 = pep438:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='test_pep438',
)
