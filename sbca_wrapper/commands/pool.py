from sbca_wrapper.command import libindy_command
from typing import Optional, Union


class Pool:

    @staticmethod
    @libindy_command('indy_create_pool_ledger_config')
    async def create_pool_config(config_name: str, config: Optional[Union[dict, str]]) -> None:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_delete_pool_ledger_config')
    async def delete_pool_config(config_name: str) -> None:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_open_pool_ledger')
    async def open_pool_connection(config_name: str, config: Optional[Union[dict, str]]) -> int:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_close_pool_ledger')
    async def close_pool_connection(pool_handle: int) -> None:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_refresh_pool_ledger')
    async def refresh_local_pool_ledger(pool_handle: int) -> None:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_list_pools')
    async def list_local_pool_ledgers() -> None:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_set_protocol_version', protocol_version=lambda arg: arg)
    async def set_protocol_version(protocol_version: int) -> None:
        """"""
        pass
