![logo](https://raw.githubusercontent.com/hyperledger/indy-node/master/collateral/logos/indy-logo.png)

#   SBCA-Indy-Wrapper
>   ***S****wisscom* ***B****lockchain* ***C****loud* ***A****uthenticator*

This project is a custom python wrapper for Hyperledger's Libindy library that aims to eventually replace the python
wrapper that is currently provided inside the [Indy SDK](https://github.com/hyperledger/indy-sdk). It is also going to
be used by our [SBCA-Indy-SDK](https://github.com/swisscom-blockchain/sbca-indy-sdk), which will be developed upon
completion / handing over of the wrapper.

##  Setup
### Requirements
*   **Python 3.6 or greater**
*   **Libindy** ([Installation Instructions](https://github.com/hyperledger/indy-sdk#installing-the-sdk))
    *   The version of the wrapper and the Libindy library should always match!

### Installation
The wrapper is an installable pip-package. Download and install it by running the following command:
```bash
pip install sbca-indy-wrapper @ git+https://github.com/swisscom-blockchain/sbca-indy-wrapper.git@v1.8.1
```

##  Usage
The package contents can be imported and used from the `sbca_wrapper` module.
```python
import sbca_wrapper

...
```

You will always be required to initialize Libindy before using it. Do so by running `initialize_libindy()` at the
beginning of your program or script. This will set the library's native logger and you can optionally set some
configuration values by passing them to the function.
```python
from sbca_wrapper import initialize_libindy

# Initializing Libindy
initialize_libindy()

...
```

To use specific parts of the wrapper, it is possible to just import the required module to do so. To use only the
wallet functions:
```python
from sbca_wrapper import initialize_libindy, Wallet

# Initializing Libindy
initialize_libindy()

# Creating Wallet
await Wallet.create_wallet({'id': 'my_wallet'}, {'key': 'my_wallet_password'})

...
```

The `sbca_wrapper` also implements custom exceptions. In order to not overload the import suggestions with tons of
exception types, they are imported as such:
```python
from sbca_wrapper.error import LibindyError, WalletNotFoundError, error_code_map

...
```
>   `LibindyError` is the parent class of all other custom exceptions implemented by the wrapper.

>   `error_code_map` is a `dict` which maps the error codes used within Libindy to their proper exception class.

##  Authors
**Lead Development**
*   Roth Jeremy ([Skilletpan](https://github.com/Skilletpan))

**Additional Development**
*   Krell Jérôme ([JeromeK13](https://github.com/JeromeK13))

**Acknowledgments**
*   Alvarado Flores Jorge - *Technical Manager*
*   Riva Luigi - *Project Owner*