from src.command import libindy_command
from typing import Optional, Union


class Wallet:

    @staticmethod
    @libindy_command('indy_create_wallet')
    async def create_wallet(wallet_config: Union[dict, str], wallet_credentials: Union[dict, str]) -> None:
        """
        Create a new secure indy wallet.

        :param wallet_config: str, dict - Wallet and wallet configuration JSON
            {
                id: str - Identifier that will also be used as the wallet's (file) name
                storage_type: str <optional, default: "default"> - Wallet storage type name
                    -> Register wallet storage types using register_wallet_storage
                storage_config: dict <optional> - Storage configuration JSON
                    -> Keys are defined by the wallet storage type
                    -> DEFAULT: {
                        path: str <optional> - Path where wallets of storage type are saved.
                            -> By default, it points to $HOME/.indy_client/wallet
                    }
            }
        :param wallet_credentials: str, dict - Wallet credential and wallet storage credential JSON
            {
                key: str - Password to open wallet and to derive keys from
                storage_credentials: dict <optional> - Credential values required by wallet storage type
                    -> For default storage type, leave empty
                key_derivation_method: str <optional, default: "ARGON2I_MOD"> - Key derivation algorithm name
                    Supported:
                     -  ARGON2I_MOD: Default method
                     -  ARGON2I_INT: Less secure, but faster
                     -  RAW: No derivation, raw key is used (generate key using generate_raw_key)
            }
        """
        pass

    @staticmethod
    @libindy_command('indy_delete_wallet')
    async def delete_wallet(wallet_config: Union[dict, str], wallet_credentials: Union[dict, str]) -> None:
        """
        Delete an indy wallet.

        :param wallet_config: str, dict - Wallet and wallet configuration JSON
            {
                id: str - Identifier of the wallet to delete
                storage_type: str <optional, default: "default"> - Wallet storage type name
                    -> Register wallet storage types using register_wallet_storage
                storage_config: dict <optional> - Storage configuration JSON
                    -> Keys are defined by the wallet storage type
                    -> DEFAULT: {
                        path: str <optional> - Path where wallets of storage type are saved.
                            -> By default, it points to $HOME/.indy_client/wallet
                    }
            }
        :param wallet_credentials: str, dict - Wallet credential and wallet storage credential JSON
            {
                key: str - Password to open wallet and to derive keys from
                storage_credentials: dict <optional> - Credential values required by wallet storage type
                    -> For default storage type, leave empty
                key_derivation_method: str <optional, default: "ARGON2I_MOD"> - Key derivation algorithm name
                    Supported:
                     -  ARGON2I_MOD: Default method
                     -  ARGON2I_INT: Less secure, but faster
                     -  RAW: No derivation, raw key is used (generate key using generate_raw_key)
            }
        """
        pass

    @staticmethod
    @libindy_command('indy_open_wallet')
    async def open_wallet(wallet_config: Union[dict, str], wallet_credentials: Union[dict, str]) -> int:
        """
        Open an indy wallet to access its contents.

        Wallets can only be opened if they have been created using the create_wallet function and are not already open.

        :param wallet_config: str, dict - Wallet and wallet configuration JSON
            {
                id: str - Identifier of the wallet to open
                storage_type: str <optional, default: "default"> - Wallet storage type name
                    -> Register wallet storage types using register_wallet_storage
                storage_config: dict <optional> - Storage configuration JSON
                    -> Keys are defined by the wallet storage type
                    -> DEFAULT: {
                        path: str <optional> - Path where wallets of storage type are saved.
                            -> By default, it points to $HOME/.indy_client/wallet
                    }
            }
        :param wallet_credentials: str, dict - Wallet credential and wallet storage credential JSON
            {
                key: str - Password to open wallet and to derive keys from
                rekey: str <optional> - New password for the wallet (will replace key)
                storage_credentials: dict <optional> - Credential values required by wallet storage type
                    -> For default storage type, leave empty
                key_derivation_method: str <optional, default: "ARGON2I_MOD"> - Key derivation algorithm name
                    Supported:
                     -  ARGON2I_MOD: Default method
                     -  ARGON2I_INT: Less secure, but faster
                     -  RAW: No derivation, raw key is used (generate key using generate_raw_key)
                rekey_derivation_method: str <optional, default: "ARGON2I_MOD"> Derivation method for rekey
            }
        :returns wallet_handle: int - Handle to the wallet that is used in calls to access the wallet's contents
        """
        pass

    @staticmethod
    @libindy_command('indy_close_wallet')
    async def close_wallet(wallet_handle: int) -> None:
        """
        Close an open wallet.

        :param wallet_handle: int - Handle of the currently open wallet
        """
        pass

    @staticmethod
    @libindy_command('indy_import_wallet')
    async def import_wallet(wallet_config: Union[dict, str], wallet_credentials: Union[dict, str],
                            import_config: Union[dict, str]) -> None:
        """
        Create a new secure indy wallet and import contents that were previously exported from another indy wallet.

        :param wallet_config: str, dict - Wallet and wallet configuration JSON
            {
                id: str - Identifier that will also be used as the wallet's (file) name
                storage_type: str <optional, default: "default"> - Wallet storage type name
                    -> Register wallet storage types using register_wallet_storage
                storage_config: dict <optional> - Storage configuration JSON
                    -> Keys are defined by the wallet storage type
                    -> DEFAULT: {
                        path: str <optional> - Path where wallets of storage type are saved.
                            -> By default, it points to $HOME/.indy_client/wallet
                    }
            }
        :param wallet_credentials: str, dict - Wallet credential and wallet storage credential JSON
            {
                key: str - Password to open wallet and to derive keys from
                storage_credentials: dict <optional> - Credential values required by wallet storage type
                    -> For default storage type, leave empty
                key_derivation_method: str <optional, default: "ARGON2I_MOD"> - Key derivation algorithm name
                    Supported:
                     -  ARGON2I_MOD: Default method
                     -  ARGON2I_INT: Less secure, but faster
                     -  RAW: No derivation, raw key is used (generate key using generate_raw_key)
            }
        :param import_config: str, dict - Data import configuration
            {
                path: str - Path to the file holding exported wallet data
                key: str - Key used to export wallet data
            }
        """
        pass

    @staticmethod
    @libindy_command('indy_export_wallet')
    async def export_wallet(wallet_handle: int, export_config: Union[dict, str]) -> None:
        """
        Export the data of a wallet into a file.

        :param wallet_handle: int - Handle of the open wallet to export data from
        :param export_config: str, dict - Data export configuration
            {
                path: str - Path to create export data file at
                key: str - Passphrase to derive wallet export key from
                key_derivation_method: str <optional, default: "ARGON2I_MOD"> - Key derivation algorithm name
                    Supported:
                     -  ARGON2I_MOD: Default method
                     -  ARGON2I_INT: Less secure, but faster
                     -  RAW: No derivation, raw key is used (generate key using generate_raw_key)
            }
        """
        pass

    @staticmethod
    @libindy_command('indy_generate_wallet_key')
    async def generate_raw_key(generator_config: Optional[Union[dict, str]]) -> str:
        """
        Generate a wallet master key using the "RAW" derivation method.
        # TODO: Why master key?

        :param generator_config: str, dict <optional> - Config for key generation
            {
                seed: str <optional> - Seed for specific key generation (UTF-8, BASE64 or HEX string)
            }
        """
        pass
