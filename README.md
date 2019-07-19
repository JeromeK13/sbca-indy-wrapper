![Hyperledger Indy Logo](https://raw.githubusercontent.com/hyperledger/indy-node/master/collateral/logos/indy-logo.png)


#   SBCA-Indy-Wrapper

[![Build Status](https://dev.azure.com/swisscomblockchain/sbca/_apis/build/status/swisscom-blockchain.sbca-indy-wrapper?branchName=dev)](https://dev.azure.com/swisscomblockchain/sbca/_build/latest?definitionId=4&branchName=dev)

This project is an enhanced version of Hyperledger's Python wrapper of the [Indy SDK](https://github.com/hyperledger/indy-sdk). It aims to provide easier usage than the original wrapper while also reducing the amount of coding required to add or edit the wrapper functions.


##  Requirements

*   **Python** (Version 3.6+)
*   **Libindy** ([Installation Instructions](https://github.com/hyperledger/indy-sdk#installing-the-sdk))


##  Installation

The SBCA-Indy-Wrapper is a `pip`-compatible Python package and can therefore be installed as such. Run the command below in the command line of your system to install the wrapper.

```shell
pip install sbca-indy-wrapper @ git+https://github.com/swisscom-blockchain/sbca-indy-wrapper.git
```


##  Usage

Use the wrapper like you would any other Python package.

```python
import sbca_wrapper


sbca_wrapper.LIBINDY.logger.info('Hello from Libindy!')
...
```

```python
from sbca_wrapper import Wallet


async def create_wallet():

    await Wallet.create_wallet(...)
    ...
```

```python
from sbca_wrapper.error import WalletNotFoundError


...
raise WalletNotFoundError
```

You can also set some of Libindy's runtime configuration values.

```python
from sbca_wrapper import LIBINDY


LIBINDY.set_runtime_config(collect_backtrace=False)
...
```

>   NOTE:   Runtime configurations have to be set **before** using any other library functions!


##  Authors
**Lead Development**
*   Roth Jeremy ([Skilletpan](https://github.com/Skilletpan))

**Additional Development**
*   Krell Jérôme ([JeromeK13](https://github.com/JeromeK13))

**Acknowledgments**
*   Alvarado Flores Jorge - *Technical Manager*
*   Riva Luigi - *Project Owner*
