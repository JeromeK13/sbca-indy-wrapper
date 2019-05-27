from ctypes import c_int32, c_uint, c_uint64
from sbca_wrapper._command import libindy_command
from typing import Optional, Union


class Anoncreds:

    @staticmethod
    @libindy_command('indy_issuer_create_schema')
    async def create_schema(issuer_schema_did: str, schema_name: str, schema_version: str,
                            schema_attributes: Union[list, str]) -> (str, dict):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_issuer_create_and_store_credential_def')
    async def create_credential_definition(wallet_handle: int, cred_def_did: str, cred_def_schema: Union[dict, str],
                                           cred_def_tag: str, cred_def_type: Optional[str],
                                           cred_def_config: Optional[Union[dict, str]]) -> (str, dict):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_issuer_create_and_store_revoc_reg')
    async def create_revocation_registry(wallet_handle: int, revoc_reg_did: str, revoc_reg_type: Optional[str],
                                         revoc_reg_tag: str, revoc_reg_cred_def_id: str,
                                         revoc_reg_config: Union[dict, str],
                                         tails_writer_handle: int) -> (str, dict, dict):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_issuer_create_credential_offer')
    async def create_credential_offer(wallet_handle: int, cred_def_id: str) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_issuer_create_credential')
    async def create_credential(wallet_handle: int, cred_offer: Union[dict, str], cred_request: Union[dict, str],
                                cred_values: Union[dict, str], revoc_reg_id: Optional[str],
                                tails_reader_handle: Optional[int]) -> (dict, Optional[str], Optional[dict]):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_issuer_revoke_credential')
    async def revoke_credential(wallet_handle: int, tails_reader_handle: int, revoc_reg_id: str,
                                cred_revoc_id: str) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_issuer_merge_revocation_registry_deltas')
    async def merge_revocation_registry_deltas(revoc_reg_delta_1: Union[dict, str],
                                               revoc_reg_delta_2: Union[dict, str]) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_create_master_secret')
    async def create_master_secret(wallet_handle: int, master_secret_name: Optional[str]) -> str:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_create_credential_req')
    async def create_credential_request(wallet_handle: int, cred_req_did: str, cred_offer: Union[dict, str],
                                        cred_def: Union[dict, str], master_secret_id: str) -> (dict, dict):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_store_credential')
    async def store_credential(wallet_handle: int, cred_id: Optional[str], cred_req_metadata: Union[dict, str],
                               cred_def: Union[dict, str], revoc_reg_def: Optional[Union[dict, str]]) -> str:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_get_credential')
    async def get_credential_by_id(wallet_handle: int, cred_id: str) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_delete_credential')
    async def delete_credential(wallet_handle: int, cred_id: str):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_get_credentials')
    async def get_credentials(wallet_handle: int, credential_filter: Union[dict, str]) -> list:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_get_credentials_for_proof_req')
    async def fetch_credentials_for_proof_request(wallet_handle: int, proof_req: Union[dict, str]) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_search_credentials', return_type=(c_int32, c_uint))
    async def open_credential_search(wallet_handle: int, cred_search_queries: Union[dict, str]) -> (int, int):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_fetch_credentials', cred_count=lambda arg: c_uint(arg))
    async def get_credentials_from_search(search_handle: int, cred_count: int) -> list:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_close_credentials_search')
    async def close_credential_search(search_handle: int):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_search_credentials_for_proof_req')
    async def open_proof_request_search(wallet_handle: int, proof_req: Union[dict, str],
                                        cred_search_queries: Union[dict, str]) -> int:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_fetch_credentials_for_proof_req', cred_count=lambda arg: c_uint(arg))
    async def get_credentials_from_proof_request_search(search_handle: int, item_id: str, cred_count: int) -> list:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_close_credentials_search_for_proof_req')
    async def close_proof_request_search(search_handle: int):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_prover_create_proof')
    async def create_proof(wallet_handle: int, proof_req: Union[dict, str], proof_creds: Union[dict, str],
                           master_secret_name: str, proof_schemas: Union[dict, str], proof_cred_defs: Union[dict, str],
                           proof_revoc_states: Union[dict, str]) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_verifier_verify_proof')
    async def verify_proof(proof_req: Union[dict, str], proof: Union[dict, str], proof_schemas: Union[dict, str],
                           proof_cred_defs: Union[dict, str], proof_revoc_reg_defs: Union[dict, str],
                           proof_revoc_regs: Union[dict, str]) -> bool:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_create_revocation_state', timestamp=lambda arg: c_uint64(arg))
    async def create_revocation_state(tails_reader_handle: int, revoc_reg_defs: Union[dict, str],
                                      revoc_reg_delta: Union[dict, str], timestamp: int, cred_revoc_id: str) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_update_revocation_state', timestamp=lambda arg: c_uint64(arg))
    async def update_revocation_state(tails_reader_handle: int, revoc_state: Union[dict, str],
                                      revoc_reg_def: Union[dict, str], revoc_reg_delta: Union[dict, str],
                                      timestamp: int, cred_revoc_id: str) -> dict:
        """"""
        pass
