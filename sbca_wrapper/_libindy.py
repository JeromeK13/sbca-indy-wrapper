import asyncio
import itertools
import json
import logging
import sys

from .error import LibindyError, error_code_map, CommonInvalidParamError
from ._logger import get_sbca_logger

from ctypes import CDLL, CFUNCTYPE, byref, c_char_p, c_int, c_void_p
from typing import Any, Callable, Dict, Tuple, Union

# Logger settings
_LOGGER = get_sbca_logger('libindy')
_NATIVE_LOGGER = get_sbca_logger('libindy.native')


def _load_library():
    # Get library name on the running OS
    try:
        lib_name = {
            'darwin': 'libindy.dylib',
            'linux': 'libindy.so',
            'linux2': 'libindy.so',
            'win32': 'indy.dll'
        }.get(sys.platform)
    except KeyError:
        _LOGGER.error(f'Libindy is not supported on the {sys.platform} operating system!\n')
        raise

    # Load library from the system
    try:
        lib = CDLL(lib_name)
    except OSError:
        _LOGGER.error(f'Could not load Libindy library from the system!\n')
        raise

    # Return library
    _LOGGER.debug('Libindy library loaded from the system')
    return lib


# Libindy library
_LIBRARY: CDLL = _load_library()


class Libindy:
    """
    Enables interactions with the installed C-library Libindy.
    """

    # Singleton instance
    _instance: 'Libindy' = None

    # Libindy instance fields
    _futures: Dict[int, Tuple[asyncio.AbstractEventLoop, asyncio.Future]] = {}
    _command_handle: itertools.count = itertools.count()

    # Libindy instance state fields
    initialized: bool = False

    # ------------------------------------------------------------------------------------------------------------------
    #  Constructor
    # ------------------------------------------------------------------------------------------------------------------
    def __new__(cls) -> 'Libindy':
        """
        Only create a new Libindy instance if none already exists

        :returns libindy: Libindy - Libindy instance
        """

        # Create new Libindy instance if none exists
        if not Libindy._instance:
            Libindy._instance = object.__new__(cls)

        # Return Libindy instance
        return Libindy._instance

    # ------------------------------------------------------------------------------------------------------------------
    #  Methods
    #
    # Libindy Commands -------------------------------------------------------------------------------------------------
    @classmethod
    def run_command(cls, command_name: str, *command_args) -> asyncio.Future:
        """
         Asynchronously run a command defined in the Libindy library.

        :param command_name: str - Libindy command name
        :param command_args - C-type encoded command arguments
        :returns command_future: Future - Future object for the command
        """

        # Raise error if Libindy is not initialized
        if not cls.initialized:
            _LOGGER.error('Libindy has to be initialized before running commands!\n')
            raise RuntimeError

        # Get Libindy command from library
        command: Callable = cls._get_command(command_name)

        # Create and store future
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        command_future: asyncio.Future = loop.create_future()
        command_handle: int = next(cls._command_handle)
        cls._futures[command_handle] = (loop, command_future)

        # Call Libindy library
        response_code: int = command(command_handle, *command_args)

        # Set exception
        if response_code != 0:
            _LOGGER.error(f'Libindy library returned non-success code {response_code}!\n')
            command_future.set_exception(Libindy._get_indy_error(response_code))

        # Return future object
        return command_future

    @classmethod
    def sync_run_command(cls, command_name: str, *command_args) -> Any:
        """
         Synchronously run a command defined in the Libindy library.

        :param command_name: str - Libindy command name
        :param command_args - C-type encoded command arguments
        :returns command_res: Any - Command response
        """
        return cls._get_command(command_name)(*command_args)

    @staticmethod
    def implements_command(command_name: str) -> bool:
        """
        Get whether a specific command is implemented in the Libindy library installed on your system.

        :param command_name: str - Command name to check
        :returns is_installed: bool - Whether the command is installed
        """
        return hasattr(_LIBRARY, command_name)

    @classmethod
    def _get_command(cls, command_name: str) -> Callable:
        if not cls.implements_command(command_name):
            _LOGGER.error(f'Command {command_name} is not implemented in the Libindy library!\n')
            raise NotImplementedError
        return getattr(_LIBRARY, command_name)

    # Command Callback -------------------------------------------------------------------------------------------------
    @classmethod
    def create_callback(cls, c_callback_signature: CFUNCTYPE, transform_fn: Callable = None) -> Any:
        """
        Create a C-encoded callback function for a Libindy command.

        :param c_callback_signature: CFUNCTYPE - C-encoded callback function signature
        :param transform_fn: function <optional> - Function to alter response values before returning
        :returns callback_function: Any - C-encoded callback function
        """

        # Define Libindy callback function
        def _callback_fn(command_handle: int, response_code: int, *response_values) -> Any:
            # Transform callback return values (if necessary)
            response_values = transform_fn(*response_values) if transform_fn is not None else response_values
            response = cls._get_indy_error(response_code)
            cls._indy_callback(command_handle, response, *response_values)

        # Call Libindy callback function with C-types
        return c_callback_signature(_callback_fn)

    @classmethod
    def _indy_callback(cls, command_handle: int, response: LibindyError, *response_values) -> None:
        loop, _ = cls._futures[command_handle]
        loop.call_soon_threadsafe(cls._indy_loop_callback, command_handle, response, *response_values)

    @classmethod
    def _indy_loop_callback(cls, command_handle: int, response: LibindyError, *response_values) -> None:
        # Get command future from futures stack
        _, future = cls._futures.pop(command_handle)

        # Set future result
        if not future.cancelled():

            # Build and return command response
            if response.indy_code == 0:
                future.set_result(None if not response_values else tuple(response_values))

            # Handle command exception
            else:
                _LOGGER.error(f'Libindy returned non-success code {response.indy_code} ({response.indy_name})!\n')
                future.set_exception(response)
        else:
            _LOGGER.debug('Command future was cancelled before callback execution\n')

    # Various ----------------------------------------------------------------------------------------------------------
    @classmethod
    def _get_indy_error(cls, code: int) -> LibindyError:

        # Return success
        if code == 0:
            return LibindyError(0, 'Success')

        # Get and return error data
        c_error = c_char_p()
        cls._get_command('indy_get_current_error')(byref(c_error))
        error_details: dict = json.loads(c_error.value.decode())

        # Get error type
        try:
            error_type: type = error_code_map[code]
        except KeyError:
            _LOGGER.error(f'Libindy responded with unknown response code {code}!\n')
            raise

        # Create and return error
        if error_type is CommonInvalidParamError:
            return error_type(code, error_details.get('message'), error_details.get('backtrace'))
        return error_type(error_details.get('message'), error_details.get('backtrace'))


def initialize_libindy(runtime_config: Union[dict, str] = None) -> None:
    """
    Initialize Libindy by setting the library logger and optionally a runtime config.

    :param runtime_config: str, dict <optional> - Runtime configuration settings for the Libindy library
        -> Will only be called when first Libindy instance is created!
        {
            crypto_thread_pool_size: int <optional, default: 4> - Thread pool size for crypto operations
            collect_backtrace: bool <optional, default: ?> - Whether to collect backtrace of library errors
        }
    """

    _LOGGER.info('Initializing Libindy')

    # Raise error if Libindy is already initialized
    if Libindy.initialized:
        _LOGGER.error('Libindy is already initialized!\n')
        raise RuntimeError

    # Set runtime config
    if runtime_config:
        _LOGGER.info(f'Setting Libindy runtime config >>> Config values: {runtime_config}')
        runtime_config: str = runtime_config if isinstance(runtime_config, str) else json.dumps(runtime_config)
        Libindy.sync_run_command('indy_set_runtime_config', c_char_p(runtime_config.encode('utf-8')))

    _LOGGER.info('Setting Libindy library logger')

    # Add log level
    logging.addLevelName(5, 'TRACE')

    # Logging function
    def _log(context, level, target, message, module_path, file, line) -> None:
        libindy_logger = _NATIVE_LOGGER.getChild(f'{target.decode().replace("::", ".")}')
        level_mapping = {1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG, 5: 5, }
        libindy_logger.log(level_mapping[level], f'{file.decode()}:{line} | {message.decode()}')

    # Define logger callback functions
    initialize_libindy.callbacks = {
        'enabled_cb': None,
        'log_cb': CFUNCTYPE(None, c_void_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int)(_log),
        'flush_cb': None
    }

    # Run indy command
    Libindy.sync_run_command('indy_set_logger', None, initialize_libindy.callbacks['enabled_cb'],
                             initialize_libindy.callbacks['log_cb'], initialize_libindy.callbacks['flush_cb'])

    # Flag Libindy as initialized
    Libindy.initialized = True
    _LOGGER.info('Finished initializing Libindy\n')
