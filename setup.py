from setuptools import setup

setup(name='sbca-indy-wrapper',
      version='1.8.1',  # Should be kept at the same version as the Libindy library
      description='A Python 3.6.5 wrapper for the Libindy library developed by Hyperledger.',
      url='https://github.com/swisscom-blockchain/sbca-indy-wrapper',
      author='Skilletpan',
      author_email='skilletpan.14@gmail.com',
      license='Apache 2.0',
      packages=['sbca_wrapper'],
      install_requires=[],
      zip_safe=False
      )
