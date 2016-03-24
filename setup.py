from setuptools import setup, find_packages

setup(
    name='xia',
    version='0.0.1',
    description='Python Framework for writing APIs',
    url='https://github.com/py-xia/xia',
    author='Brian de Heus',
    author_email='me@brian.jp',
    license='MIT',
    install_requires=['tornado'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
