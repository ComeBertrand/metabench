from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import io
import sys

import metabench


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')


class PyTest(TestCommand):
    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='metabench',
    version=metabench.__version__,
    url='https://github.com/ComeBertrand/metabench/',
    license='MIT License',
    author='Come Bertrand',
    tests_require=['pytest'],
    install_requires=['numpy>=1.11.2',
                      'decorator>=4.0.11'],
    cmdclass={'test': PyTest},
    author_email='bertrand.cosme@gmail.com',
    description='Automated benchmarks of metaheuristics performance',
    long_description=long_description,
    packages=['metabench'],
    include_package_data=True,
    platforms='any',
    test_suite='metabench.test.test_metabench',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    extras_require={'testing': ['pytest']}
)
