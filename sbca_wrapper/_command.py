import inspect
import json
import time

from ._libindy import Libindy
from ._logger import get_sbca_logger

from ctypes import CFUNCTYPE, POINTER, c_bool, c_char_p, c_int32, c_uint8, c_uint32
from functools import wraps
from typing import Any, Callable, Dict, List, Union

_LIBINDY_LOGGER = get_sbca_logger('libindy')
_LOGGER = _LIBINDY_LOGGER.getChild('command')

_return_types: Dict[type, Any] = {str: c_char_p, int: c_int32, bool: c_bool, bytes: (POINTER(c_uint8), c_uint32)}
_encoders: Dict[type, Callable] = {
    str: lambda arg: c_char_p(arg.encode('utf-8')),
    int: lambda arg: c_int32(arg),
    bool: lambda arg: c_bool(arg),
    bytes: lambda arg: (arg, c_uint32(len(arg))),
    Union[dict, str]: lambda arg: _encoders[str](json.dumps(arg) if isinstance(arg, dict) else arg),
    Union[list, str]: lambda arg: _encoders[str](json.dumps(arg) if isinstance(arg, list) else arg),
}


def _parse_optional_type(parse_type: Union) -> (type, bool):
    if str(parse_type).startswith('typing.Union') and type(None) in parse_type.__args__:
        return Union[tuple(filter(lambda t: not isinstance(None, t), parse_type.__args__))], True
    return parse_type, False


def libindy_command(libindy_command_name: str, return_type: tuple = None, **argument_encoders) -> Callable:
    # Assert command is implemented
    try:
        assert Libindy.implements_command(libindy_command_name)
    except AssertionError:
        _LOGGER.error(f'Command {libindy_command_name} is not implemented in Libindy library!\n')
        raise

    def _inner_libindy_command(command_signature: callable) -> Callable:

        _LOGGER.info(f'Building command {command_signature.__qualname__}')

        # Function argument type annotations
        command_arguments = inspect.getfullargspec(command_signature).args
        command_annotations = inspect.getfullargspec(command_signature).annotations

        # Assert return type is specified
        try:
            assert 'return' in command_annotations.keys()
        except AssertionError:
            _LOGGER.error(f'Return type specification for command {command_signature.__qualname__} is missing!\n')
            raise

        # Assert argument types are specified
        try:
            assert set(command_arguments).issubset(command_annotations.keys())
        except AssertionError:
            missing_args = list(filter(lambda arg: arg not in command_annotations.keys(), command_arguments))
            _LOGGER.error(f'Argument type specification for arguments {str(missing_args)} of command '
                          f'{command_signature.__qualname__} are missing!\n')
            raise

        # Map return annotation to tuple
        if not isinstance(command_annotations['return'], tuple):
            command_annotations['return'] = (command_annotations['return'],) if command_annotations['return'] else ()

        # Libindy command declaration
        @wraps(command_signature)
        async def _command(*args, **kwargs) -> Any:

            # Get starting time for time measuring
            starting_time = time.clock()

            # Map args to kwargs
            _args = list(args)
            for _arg_name in list(filter(lambda _n: _n not in kwargs.keys(), _command.arguments)):
                kwargs[_arg_name] = kwargs.get(_arg_name, _args.pop(0))

            # Build kwargs string for logging
            if not kwargs:
                kwargs_string = None
            else:
                kwargs_string = ', '.join(list(map(lambda _key: f'{_key}: {kwargs[_key]}', command_arguments)))
            _LIBINDY_LOGGER.info(f'{command_signature.__qualname__} >>> Args: {kwargs_string}')

            # Encode args to C-types
            _enc = []
            for _arg_name in _command.arguments:
                _arg_enc = _command.parsers[_arg_name](kwargs[_arg_name])
                _enc.extend(_arg_enc) if isinstance(_arg_enc, tuple) else _enc.append(_arg_enc)

            # Run Libindy command
            _res = await Libindy.run_command(libindy_command_name, *_enc, _command.callback)

            # Decode response
            _res_dec = None if not _res else tuple(_dec(_e) for _dec, _e in zip(_command.parsers['return'], _res))

            # Return response
            running_time = time.clock() - starting_time
            _LIBINDY_LOGGER.info(f'{command_signature.__qualname__} ({running_time:.2f}s) <<< Res: {_res_dec}')
            return None if not _res else _res_dec[0] if len(_res_dec) == 1 else _res_dec

        # Value parser container
        _command.parsers: dict = {'return': []}
        _command.arguments: List[str] = list(command_arguments)

        # Build C return types and callback function
        _LOGGER.info(f'Parsing C-types for command {command_signature.__qualname__}')
        return_c_types = [] if not return_type else return_type
        for command_return_type in command_annotations['return']:

            # Get if return type is optional and remove None from Union if it is
            _parsed = _parse_optional_type(command_return_type)
            _type, _optional = _parsed[0], _parsed[1]

            # Assert return type is supported
            try:
                assert return_type or _type in _return_types.keys()
            except AssertionError:
                _LOGGER.error(f'Return type {_type} is not supported by the Libindy library!\n')
                raise

            # Get C-return type
            if not return_type:
                _c_type = _return_types[_type]
                return_c_types.append(_c_type) if not isinstance(_c_type, tuple) else return_c_types.extend(_c_type)

            # Set response decode function
            if _type is str:
                if _optional:
                    _command.parsers['return'].append(lambda res: res.decode() if res else None)
                else:
                    _command.parsers['return'].append(lambda res: res.decode())
            else:
                _command.parsers['return'].append(lambda res: res)

        # Build callback (and callback transform) function
        _LOGGER.info(f'Building callback function for command {command_signature.__qualname__}')
        callback_transform = None
        if bytes in command_annotations['return']:

            # Build callback transform function
            def callback_transform(*callback_args) -> Any:
                callback_args, transformed_args = list(callback_args), []
                for index, _cb_type in enumerate(callback_transform.returns):

                    # Append bytes arguments as bytes object (pop length from following list entry)
                    if _cb_type is bytes:
                        transformed_args.append(bytes(callback_args[index][:callback_args.pop(index + 1)]))
                        continue

                    # Append non-bytes arguments as they are
                    transformed_args.append(callback_args[index])

                # Return response argument(s) as single argument or as tuple
                return transformed_args[0] if len(transformed_args) == 1 else tuple(transformed_args)

            callback_transform.returns = command_annotations['return']

        # Build callback function
        _command.callback = Libindy.create_callback(CFUNCTYPE(None, c_int32, c_int32, *return_c_types),
                                                    callback_transform)

        # Map argument encoders
        _LOGGER.info(f'Parsing argument encoder functions for command {command_signature.__qualname__}')
        for _name in command_arguments:

            _type, _optional = _parse_optional_type(command_annotations[_name])

            # Assert C-type is supported or custom encoding function is provided
            try:
                assert _name in argument_encoders.keys() or _type in _encoders.keys()
            except AssertionError:
                _LOGGER.error(f'Argument type {_type} is not supported by Libindy!\n')
                raise

            # Set custom encoding functions if provided
            if _name in argument_encoders.keys():
                _command.parsers[_name] = argument_encoders[_name]
                continue

            # Set encoding function that fits argument type
            _encoder = _encoders[_type]
            _command.parsers[_name] = _encoder if not _optional else lambda arg: None if not arg else _encoder(arg)

        return _command

    return _inner_libindy_command
