from ctypes import c_uint
from sbca_wrapper._command import libindy_command
from typing import Optional, Union


class NonSecrets:

    @staticmethod
    @libindy_command('indy_add_wallet_record')
    async def add_wallet_record(wallet_handle: int, record_type: str, record_id: str, record_value: str,
                                record_tags: Optional[Union[dict, str]]):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_update_wallet_record_value')
    async def update_wallet_record_value(wallet_handle: int, record_type: str, record_id: str,
                                         record_value: str):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_update_wallet_record_tags')
    async def update_wallet_record_tags(wallet_handle: int, record_type: str, record_id: str,
                                        record_tags: Union[dict, str]):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_add_wallet_record_tags')
    async def add_wallet_record_tags(wallet_handle: int, record_type: str, record_id: str,
                                     record_tags: Union[dict, str]):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_delete_wallet_record_tags')
    async def delete_wallet_record_tags(wallet_handle: int, record_type: str, record_id: str,
                                        record_tag_names: Union[list, str]):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_delete_wallet_record')
    async def delete_wallet_record(wallet_handle: int, record_type: str, record_id: str):
        """"""
        pass

    @staticmethod
    @libindy_command('indy_get_wallet_record')
    async def get_wallet_record(wallet_handle: int, record_type: str, record_id: str,
                                retrieve_options: Union[dict, str]) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_open_wallet_search')
    async def open_wallet_search(wallet_handle: int, record_type: str, search_queries: Union[dict, str],
                                 retrieve_options: Union[dict, str]) -> int:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_fetch_wallet_search_next_records', record_count=lambda arg: c_uint(arg))
    async def fetch_wallet_record_from_search(wallet_handle: int, search_handle: int, record_count: int) -> dict:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_close_wallet_search')
    async def close_wallet_search(search_handle: int):
        """"""
        pass
