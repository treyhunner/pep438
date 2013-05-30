from setuptools import setup, find_packages
import pep438


setup(
    name='pep438',
    version=pep438.__version__,
    author='Trey Hunner',
    url="https://github.com/treyhunner/pep438",
    description="Check your requirements for proper PEP 438 usage.",
    long_description='\n\n'.join((
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    )),
    license=open('LICENSE').read(),
    packages=find_packages(),
    py_modules=['pep438'],
    include_package_data=True,
    install_requires=[
        'requirements-parser==0.0.4',
        'clint',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'pep438 = pep438.main:main',
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
        'Programming Language :: Python :: 3.3',
    ],
    tests_require=["mock==1.0.1"],
    test_suite='test_pep438',
)
