from sbca_wrapper._command import libindy_command
from typing import Optional, Union


class Pool:
    """A class holding all indy pool functions.

    This class holds all functions required to connect to and interact with an
    indy node pool.
    """

    @staticmethod
    @libindy_command('indy_create_pool_ledger_config')
    async def create_pool_config(config_name: str, config: Optional[Union[dict, str]]):
        """Creates a new pool connection configuration.

        :param config_name: The name to set for the pool configuration. It can
            be set independently of what the pool is called otherwise, as long
            as the name is unique locally.
        :param config: The pool configuration values in the form of a dict or a
            stringified JSON object. It can be left empty or set to None to use
            the default pool configuration.

            Keys:
                genesis_txn: The path to the file with the target pool's genesis
                    transactions. If no file exists at the specified path, a
                    default genesis file will be created. The file name is
                    included in the path, so if you set the path to
                    "usr/pool/genesis", it will look for a file called "genesis"
                    at the location "usr/pool"!

        FIXME: Not specifying the genesis transaction path does not work!

        :raises PoolConfigAlreadyExistsError: Raised if a pool configuration
            with the specified name already exists.
        """
        pass

    @staticmethod
    @libindy_command('indy_delete_pool_ledger_config')
    async def delete_pool_config(config_name: str):
        """Deletes a local pool connection configuration.

        This will delete a pool connection configuration from your system. The
        pool itself or the genesis transaction file (if present) will not be
        affected.

        :param config_name: Name of the pool connection configuration to delete.

        :raises CommonInvalidStateError: Raised if trying to delete the
            configuration of a pool while a connection to that pool is open.
        """
        pass

    @staticmethod
    @libindy_command('indy_open_pool_ledger')
    async def open_pool_connection(config_name: str, config: Optional[Union[dict, str]]) -> int:
        """Opens a connection to an indy pool.

        :param config_name: Name of the target pool's configuration.
        :param config: Connection options in the form of a dict or a stringified
            JSON object.

            Keys:
                timeout: (optional integer) Time in seconds after which a
                    timeout exception will be raised.
                timeout_extended: (optional integer) Extended time in seconds
                    after which a timeout exception will be raised.
                preordered_nodes: Optional list of node names that will be
                    prioritized when attempting to connect to the pool. The
                    earlier a node stands in the list, the higher is its
                    connection priority. Nodes that are not mentioned in the
                    list will be placed at a random position after the listed
                    nodes. If no list is specified, the node priorities will
                    be assigned randomly as well.

        :raises PoolConfigNotFoundError: Raised if trying to connect to a pool
            that has not been configured on the system.
        :raises InvalidPoolHandleError: Raised if there already is an open
            connection to the target pool.

        :returns pool_handle: The handle of the pool connection.
        """
        pass

    @staticmethod
    @libindy_command('indy_close_pool_ledger')
    async def close_pool_connection(pool_handle: int):
        """Closes an open pool connection.

        This will close the connection to a pool, invalidate the pool handle and
        free the allocated resources.

        :param pool_handle: The pool connection handle to be closed.

        :raises InvalidPoolHandleError: Raised when no pool connection is open
            on the specified handle.
        """
        pass

    @staticmethod
    @libindy_command('indy_refresh_pool_ledger')
    async def refresh_local_pool_ledger(pool_handle: int):
        """
        TODO
        """
        pass

    @staticmethod
    @libindy_command('indy_list_pools')
    async def list_local_pool_ledgers():
        """Lists the names of the local pool configurations."""
        pass

    @staticmethod
    @libindy_command('indy_set_protocol_version', protocol_version=lambda arg: arg)
    async def set_protocol_version(protocol_version: int):
        """Sets the Libindy protocol version.

        This will configure Libindy to be compatible with specific node
        versions. It has to be set to match with the protocol version of the
        pool the program is interacting.

        :param protocol_version: The version that Libindy should use.
            - Protocol version 1 for indy node version 1.3
            - Protocol version 2 for indy node version 1.4 and greater
        """
        pass
