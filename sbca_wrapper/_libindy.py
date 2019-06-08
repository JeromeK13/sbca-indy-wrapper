import itertools
import json
import logging
import sys

from .error import LibindyError, CommonInvalidParamError, error_code_map
from ._logger import get_sbca_logger

from asyncio import AbstractEventLoop, Future, get_event_loop
from ctypes import CDLL, CFUNCTYPE, byref, c_char_p, c_int, c_void_p
from typing import Any, Callable, Dict, Optional, Tuple, Union

# Logger settings
_LOGGER = get_sbca_logger('libindy')
_NATIVE_LOGGER = get_sbca_logger('libindy.native')


def _load_libindy_library():
    """Loads the Libindy library into the Python context."""

    # Define supported platforms with according library name
    lib_names = {
        'darwin': 'libindy.dylib',
        'linux': 'libindy.so',
        'linux2': 'libindy.so',
        'win32': 'indy.dll'
    }

    # Raise error if platform is not supported
    if sys.platform not in lib_names.keys():
        msg = f'Libindy does not support your operating system!'
        _LOGGER.error(f'{msg}\n')
        raise OSError(msg)

    # Load library from the system
    try:
        lib = CDLL(lib_names.get(sys.platform))
    except OSError as error:
        _LOGGER.error(f'Failed to load Libindy:\n\n'
                      f'{error.strerror}')
        raise

    # Return library
    _LOGGER.info('Libindy library loaded.')
    return lib


class Libindy:
    """Holds the functions for Libindy interactions."""

    _INSTANCE: 'Libindy' = None
    _INITIALIZED: bool = False
    _LIBRARY: CDLL = _load_libindy_library()
    _FUTURES: Dict[int, Tuple[AbstractEventLoop, Future]] = {}
    _COMMAND_HANDLE_GENERATOR: itertools.count = itertools.count()

    # -------------------------------------------------------------------------
    #  Constructor
    # -------------------------------------------------------------------------
    def __new__(
            cls
    ) -> 'Libindy':
        """Ensures that only one instance of Libindy exists during runtime."""
        if not Libindy._INSTANCE:
            Libindy._INSTANCE = object.__new__(cls)
        return Libindy._INSTANCE

    def __init__(
            self,
            runtime_config: Optional[Union[dict, str]] = None
    ):
        """Sets the Libindy runtime configs and native logger.
        -----------------------------------------------------------------------
        :param runtime_config: dict, str - Runtime configuration settings
            {
                crypto_thread_pool_size: int (optional) - Thread pool size for
                    crypto operations
                     -> DEFAULT: 4
                collect_backtrace: bool (optional) - Whether to collect
                    backtrace of Libindy errors
            }
        """

        if not Libindy._INITIALIZED:
            _LOGGER.info('Initializing Libindy...')

            # Runtime Config --------------------------------------------------
            if runtime_config:
                _LOGGER.info('  Setting runtime config...')
                if isinstance(runtime_config, dict):
                    runtime_config = json.dumps(runtime_config)
                command = self._get_command('indy_set_runtime_config')
                command(c_char_p(runtime_config.encode('utf-8')))
                _LOGGER.info('  Runtime config set.')

            # Native Logger ---------------------------------------------------
            _LOGGER.info('  Setting native logger...')
            logging.addLevelName(5, 'TRACE')

            # Native logging function
            def _log(context, level, target, message, module_path, file, line):
                libindy_logger = _NATIVE_LOGGER.getChild(
                    target.decode().replace("::", ".")
                )
                level_mapping = {
                    1: logging.ERROR,
                    2: logging.WARNING,
                    3: logging.INFO,
                    4: logging.DEBUG,
                    5: 5
                }
                libindy_logger.log(
                    level_mapping[level],
                    f'{file.decode()}:{line} | {message.decode()}'
                )

            # Set persistent logger callback
            self._logger_callback = CFUNCTYPE(None, c_void_p, c_int, c_char_p,
                                              c_char_p, c_char_p, c_char_p,
                                              c_int)(_log)

            command = self._get_command('indy_set_logger')
            command(None, None, self._logger_callback, None)
            _LOGGER.info('  Native logger set.')

            Libindy._INITIALIZED = True
            _LOGGER.info('Libindy initialized.')
        else:
            _LOGGER.warning('Libindy is already initialized!')

    # -------------------------------------------------------------------------
    #  Properties
    # -------------------------------------------------------------------------
    @property
    def logger(self) -> logging.Logger:
        return _LOGGER

    @property
    def native_logger(self) -> logging.Logger:
        return _NATIVE_LOGGER

    # -------------------------------------------------------------------------
    #  Methods
    # -------------------------------------------------------------------------
    @classmethod
    def run_command(
            cls,
            command_name: str,
            *command_args
    ) -> Future:
        """Asynchronously runs a Libindy command.
        -----------------------------------------------------------------------
        :param command_name: str - The name of the Libindy command
        :param command_args - The command's C-type encoded arguments
        -----------------------------------------------------------------------
        :returns command_future: Future - The Future object for the command
        -----------------------------------------------------------------------
        :raises RuntimeError - Libindy has not been initialized
            ->  Run Libindy() when starting up your application
        """

        # Raise error if Libindy is not initialized
        if not Libindy._INITIALIZED:
            msg = 'Libindy is not initialized! Try running Libindy() during ' \
                  'application startup.'
            _LOGGER.error(f'{msg}\n')
            raise RuntimeError(msg)

        # Get Libindy command from library
        command: Callable = cls._get_command(command_name)

        # Create and store future
        loop: AbstractEventLoop = get_event_loop()
        command_future: Future = loop.create_future()
        command_handle: int = next(Libindy._COMMAND_HANDLE_GENERATOR)
        Libindy._FUTURES[command_handle] = (loop, command_future)

        # Call Libindy library
        response_code: int = command(command_handle, *command_args)

        # Set exception
        if response_code != 0:
            msg = f'Libindy library returned non-success code {response_code}!'
            _LOGGER.error(f'{msg}\n')
            command_future.set_exception(cls._get_indy_error(response_code))

        # Return future object
        return command_future

    @classmethod
    def create_command_callback(
            cls,
            callback_signature: CFUNCTYPE,
            callback_transform_function: Callable = None
    ) -> Any:
        """Creates a callback function for a Libindy command.
        -----------------------------------------------------------------------
        :param callback_signature: CFUNCTYPE - The callback function signature
        :param callback_transform_function: Callable - The callback transform
            function
        -----------------------------------------------------------------------
        :returns: callback: Callable - The callback function
        """

        def callback(handle: int, code: int, *values) -> Any:
            if callback_transform_function:
                values = callback_transform_function(*values)
            response = Libindy._get_indy_error(code)
            Libindy._run_callback(handle, response, *values)

        return callback_signature(callback)

    @classmethod
    def implements_command(
            cls,
            command_name: str
    ) -> bool:
        """Checks if Libindy implements a specific command.
        -----------------------------------------------------------------------
        :param command_name: str - The name of the command
        -----------------------------------------------------------------------
        :returns: is_implemented: bool - Whether the command is implemented
        """
        return hasattr(Libindy._LIBRARY, command_name)

    # Private -----------------------------------------------------------------
    @classmethod
    def _get_command(
            cls,
            command_name: str
    ) -> Callable:
        if not cls.implements_command(command_name):
            msg = f'Libindy does not implement {command_name}!'
            _LOGGER.error(f'{msg}\n')
            raise NotImplementedError(msg)
        return getattr(Libindy._LIBRARY, command_name)

    @classmethod
    def _run_callback(
            cls,
            command_handle: int,
            response_object: LibindyError,
            *response_values
    ):
        loop, _ = Libindy._FUTURES[command_handle]
        loop.call_soon_threadsafe(cls._loop_callback, command_handle,
                                  response_object, *response_values)

    @classmethod
    def _loop_callback(
            cls,
            command_handle: int,
            response_object: LibindyError,
            *response_values
    ):
        _, future = Libindy._FUTURES.pop(command_handle)
        response_values = None if not response_values else response_values

        if not future.cancelled():
            if response_object.indy_code == 0:
                future.set_result(response_values)
            else:
                _LOGGER.error(f'Libindy responded with non-success code '
                              f'{response_object.indy_code} '
                              f'({response_object.indy_name})!\n')
                future.set_result(response_object)
        else:
            _LOGGER.warning(
                'Future was cancelled before callback execution!\n'
            )

    # Various -----------------------------------------------------------------
    @classmethod
    def _get_indy_error(
            cls,
            response_code: int
    ) -> LibindyError:

        # Return success
        if response_code == 0:
            return LibindyError(0, 'Success')

        # Get and return error data
        c_error = c_char_p()
        cls._get_command('indy_get_current_error')(byref(c_error))
        error_details: dict = json.loads(c_error.value.decode())

        # Get error type
        if response_code not in error_code_map.keys():
            msg = f'Libindy responded with unknown response code ' \
                f'{response_code}!'
            _LOGGER.error(f'{msg}\n')
            raise KeyError(msg)

        error_type: type = error_code_map.get(response_code)

        # Create and return error
        if error_type is CommonInvalidParamError:
            return error_type(response_code, error_details.get('message'),
                              error_details.get('backtrace'))
        return error_type(error_details.get('message'),
                          error_details.get('backtrace'))
