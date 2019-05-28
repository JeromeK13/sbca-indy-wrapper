from setuptools import setup, find_packages

setup(name='sbca-indy-wrapper',
      version='1.8.1.0',
      description='A Python 3.6 wrapper for the Libindy library developed by Hyperledger.',
      url='https://github.com/swisscom-blockchain/sbca-indy-wrapper',
      author='Skilletpan',
      author_email='skilletpan.14@gmail.com',
      license='Apache 2.0',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent'
      ],
      zip_safe=False
      )
