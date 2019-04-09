from sbca_wrapper._command import libindy_command
from typing import Optional


class Pairwise:

    @staticmethod
    @libindy_command('indy_is_pairwise_exists')
    async def pairwise_exists(wallet_handle: int, foreign_did: str) -> bool:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_create_pairwise')
    async def create_pairwise(wallet_handle: int, foreign_did: str, my_did: str, metadata: Optional[str]) -> None:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_list_pairwise')
    async def list_pairwise(wallet_handle: int) -> str:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_get_pairwise')
    async def get_pairwise() -> str:
        """"""
        pass

    @staticmethod
    @libindy_command('indy_set_pairwise_metadata')
    async def set_pairwise_metadata(wallet_handle: int, foreign_did: str, metadata: Optional[str]) -> None:
        """"""
        pass
