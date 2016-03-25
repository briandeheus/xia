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
    tests_require=['tornado', 'nose'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Frameworks',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
)
