from sbca_wrapper._command import libindy_command
from typing import Union


class DID:

    @staticmethod
    @libindy_command('indy_create_and_store_my_did')
    async def create_and_store_did(
            wallet_handle: int,
            did_json: Union[dict, str]
    ) -> (str, str):
        """Creates a new DID.
        -----------------------------------------------------------------------
        # TODO: Write description if needed
        -----------------------------------------------------------------------
        :param wallet_handle: int - The handle of the wallet
            ->  Created by Wallet.open_wallet()
        :param did_json: dict - Identity information as json
            {
                # TODO: Find better description for did-key
                "did": str (optional) - If not provided the first 16 bit of
                    the verkey will be used as new DID.
                "seed": str (optional) - If not set random one will be created
                "crypto_type": str (optional) - If not set
                    ed25519 curve will be used.
                    Only ed25519 is currently supported
                # TODO: Find better description for cid-key
                "cid":  bool (optional) - If not set false will be used
            }
        -----------------------------------------------------------------------
        :returns: (
          DID: str - The newly created DID
          verkey: str - The newly created verkey
        )
        """
        pass

    @staticmethod
    @libindy_command('indy_replace_keys_start')
    async def replace_keys_start(wallet_handle: int, signing_did: str,
                                 did_json: Union[dict, str]) -> str:
        pass

    @staticmethod
    @libindy_command('indy_replace_keys_apply')
    async def replace_keys_apply(wallet_handle: int, resolve_did: str):
        pass

    @staticmethod
    @libindy_command('indy_store_their_did')
    async def store_foreign_did(wallet_handle: int,
                                did_json: Union[dict, str]):
        pass

    @staticmethod
    @libindy_command('indy_create_key')
    async def create_new_keys(wallet_handle: int,
                              did_json: Union[dict, str]) -> str:
        pass

    @staticmethod
    @libindy_command('indy_set_did_metadata')
    async def set_did_metadata(wallet_handle: int, did: str, metadata: str):
        pass

    @staticmethod
    @libindy_command('indy_get_did_metadata')
    async def get_did_metadata(wallet_handle: int, did: str) -> str:
        pass

    @staticmethod
    @libindy_command('indy_get_my_did_with_meta')
    async def get_did_with_metadata(wallet_handle: int, did: str) -> dict:
        pass

    @staticmethod
    @libindy_command('indy_list_my_dids_with_meta')
    async def get_dids_with_metadata(wallet_handle: int) -> list:
        pass

    @staticmethod
    @libindy_command('indy_set_key_metadata')
    async def set_verkey_metadata(wallet_handle: int, verkey: str,
                                  metadata: str):
        pass

    @staticmethod
    @libindy_command('indy_get_key_metadata')
    async def get_verkey_metadata(wallet_handle: int, verkey: str) -> str:
        pass

    @staticmethod
    @libindy_command('indy_key_for_did')
    async def get_did_verkey(pool_handle: int, wallet_handle: int,
                             did: str) -> str:
        pass

    @staticmethod
    @libindy_command('indy_key_for_local_did')
    async def get_local_did_verkey(wallet_handle: int, did: str) -> str:
        pass

    @staticmethod
    @libindy_command('indy_set_endpoint_for_did')
    async def set_did_endpoint(wallet_handle: int, did: str, did_url: str,
                               did_verkey: str):
        pass

    @staticmethod
    @libindy_command('indy_get_endpoint_for_did')
    async def get_did_endpoint(wallet_handle: int, pool_handle: int,
                               did: str) -> (str, str):
        pass

    @staticmethod
    @libindy_command('indy_abbreviate_verkey')
    async def abbreviate_verkey(did: str, verkey: str) -> str:
        pass
