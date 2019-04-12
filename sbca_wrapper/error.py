from typing import Dict


# Base Error
class LibindyError(Exception):

    # ------------------------------------------------------------------------------------------------------------------
    #  Constructor
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, indy_code: int, indy_name: str, message: str = None, backtrace: str = None) -> None:
        """"""

        # Build default message
        message = message if message else f'Libindy raised an error {indy_name} ({indy_code})!'
        super().__init__(message)

        # Property assignments
        self._indy_code: int = indy_code
        self._indy_name: str = indy_name
        self._message: str = message
        self._trace: str = backtrace
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #  Properties
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def indy_code(self) -> int: return self._indy_code

    @property
    def indy_name(self) -> str: return self._indy_name

    @property
    def message(self) -> str: return self._message

    @property
    def backtrace(self) -> str: return self._trace


# Common Errors --------------------------------------------------------------------------------------------------------
class CommonInvalidParamError(LibindyError):
    def __init__(self, indy_code: int, message: str = None, backtrace: str = None) -> None:
        if indy_code not in range(100, 111):
            raise RuntimeError(f'CommonInvalidParam error code has to be between 100 and 111; got {indy_code}!')
        if not message:
            message = f'Libindy command received invalid parameter {indy_code - 99}!'
        super().__init__(indy_code, f'CommonInvalidParam{indy_code - 99}', message, backtrace)
        self._param_index: int = indy_code - 99


class CommonInvalidStateError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(112, 'CommonInvalidState', message, backtrace)


class CommonInvalidStructureError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(113, 'CommonInvalidStructure', message, backtrace)


class CommonIOError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(114, 'CommonIOError', message, backtrace)


# Wallet Errors --------------------------------------------------------------------------------------------------------
class InvalidWalletHandleError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(200, 'WalletInvalidHandle', message, backtrace)


class UnknownWalletTypeError(LibindyError):
    def __init__(self, message: str, backtrace: str = None) -> None:
        super().__init__(201, 'WalletUnknownTypeError', message, backtrace)


class WalletTypeAlreadyRegisteredError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(202, 'WalletTypeAlreadyRegisteredError', message, backtrace)


class WalletAlreadyExistsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(203, 'WalletAlreadyExistsError', message, backtrace)


class WalletNotFoundError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(204, 'WalletNotFoundError', message, backtrace)


class WalletIncompatibleWithPoolError(LibindyError):
    """
    NOTE: Error type is never used in Libindy. Deprecated?
    """
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(205, 'WalletIncompatiblePoolError', message, backtrace)


class WalletAlreadyOpenError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(206, 'WalletAlreadyOpenedError', message, backtrace)


class InvalidWalletCredentialsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(207, 'WalletAccessFailed', message, backtrace)


class WalletInputError(LibindyError):
    """
    NOTE: Error type is never used in Libindy. Deprecated?
    """
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(208, 'WalletInputError', message, backtrace)


class WalletDecodingError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(209, 'WalletDecodingError', message, backtrace)


class WalletStorageError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(210, 'WalletStorageError', message, backtrace)


class WalletEncryptionError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(211, 'WalletEncryptionError', message, backtrace)


class WalletItemNotFoundError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(212, 'WalletItemNotFound', message, backtrace)


class WalletItemAlreadyExistsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(213, 'WalletItemAlreadyExists', message, backtrace)


class BadWalletQueryError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(214, 'WalletQueryError', message, backtrace)


# Pool and Ledger Errors -----------------------------------------------------------------------------------------------
class PoolConfigNotFoundError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(300, 'PoolLedgerNotCreatedError', message, backtrace)


class InvalidPoolHandleError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(301, 'PoolLedgerInvalidPoolHandle', message, backtrace)


class PoolLedgerTerminatedError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(302, 'PoolLedgerTerminated', message, backtrace)


class NoLedgerConsensusError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(303, 'LedgerNoConsensusError', message, backtrace)


class InvalidLedgerTransactionError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(304, 'LedgerInvalidTransaction', message, backtrace)


class InsufficientPrivilegesError(LibindyError):
    """
    NOTE: Error type is never used in Libindy. Deprecated?
    """
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(305, 'LedgerSecurityError', message, backtrace)


class PoolConfigAlreadyExistsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(306, 'PoolLedgerConfigAlreadyExistsError', message, backtrace)


class PoolConnectionTimeoutError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(307, 'PoolLedgerTimeout', message, backtrace)


class IncompatibleProtocolVersionError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(308, 'PoolIncompatibleProtocolVersion', message, backtrace)


class LedgerItemNotFoundError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(309, 'LedgerNotFound', message, backtrace)


# Anoncreds Errors -----------------------------------------------------------------------------------------------------
class RevocationRegistryFullError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(400, 'AnoncredsRevocationRegistryFullError', message, backtrace)


class InvalidUserRevocationIdError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(401, 'AnoncredsInvalidUserRevocId', message, backtrace)


class MasterSecretNameAlreadyExistsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(404, 'AnoncredsMasterSecretDuplicateNameError', message, backtrace)


class ProofRejectedError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(405, 'AnoncredsProofRejected', message, backtrace)


class CredentialRevokedError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(406, 'AnoncredsCredentialRevoked', message, backtrace)


class CredentialDefinitionAlreadyExistsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(407, 'AnoncredsCredDefAlreadyExistsError', message, backtrace)


# Crypto Errors --------------------------------------------------------------------------------------------------------
class UnknownCryptoTypeError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(500, 'UnknownCryptoTypeError', message, backtrace)


class DIDAlreadyExistsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(600, 'DidAlreadyExistsError', message, backtrace)


class UnknownPaymentMethodError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(700, 'PaymentUnknownMethodError', message, backtrace)


class IncompatiblePaymentMethodsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(701, 'PaymentIncompatibleMethodsError', message, backtrace)


class InsufficientFundsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(702, 'PaymentInsufficientFundsError', message, backtrace)


class PaymentSourceDoesNotExistError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(703, 'PaymentSourceDoesNotExistError', message, backtrace)


class PaymentOperationNotSupportedError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(704, 'PaymentOperationNotSupportedError', message, backtrace)


class ExtraFundsError(LibindyError):
    def __init__(self, message: str = None, backtrace: str = None) -> None:
        super().__init__(705, 'PaymentExtraFundsError', message, backtrace)


# Map error type to error code -----------------------------------------------------------------------------------------
error_code_map: Dict[int, type] = {
    100: CommonInvalidParamError,
    101: CommonInvalidParamError,
    102: CommonInvalidParamError,
    103: CommonInvalidParamError,
    104: CommonInvalidParamError,
    105: CommonInvalidParamError,
    106: CommonInvalidParamError,
    107: CommonInvalidParamError,
    108: CommonInvalidParamError,
    109: CommonInvalidParamError,
    110: CommonInvalidParamError,
    111: CommonInvalidParamError,
    112: CommonInvalidStateError,
    113: CommonInvalidStructureError,
    114: CommonIOError,
    200: InvalidWalletHandleError,
    201: UnknownWalletTypeError,
    202: WalletTypeAlreadyRegisteredError,
    203: WalletAlreadyExistsError,
    204: WalletNotFoundError,
    205: WalletIncompatibleWithPoolError,
    206: WalletAlreadyOpenError,
    207: InvalidWalletCredentialsError,
    208: WalletInputError,
    209: WalletDecodingError,
    210: WalletStorageError,
    211: WalletEncryptionError,
    212: WalletItemNotFoundError,
    213: WalletItemAlreadyExistsError,
    214: BadWalletQueryError,
    300: PoolConfigNotFoundError,
    301: InvalidPoolHandleError,
    302: PoolLedgerTerminatedError,
    303: NoLedgerConsensusError,
    304: InvalidLedgerTransactionError,
    305: InsufficientPrivilegesError,
    306: PoolConfigAlreadyExistsError,
    307: PoolConnectionTimeoutError,
    308: IncompatibleProtocolVersionError,
    309: LedgerItemNotFoundError,
    400: RevocationRegistryFullError,
    401: InvalidUserRevocationIdError,
    404: MasterSecretNameAlreadyExistsError,
    405: ProofRejectedError,
    406: CredentialRevokedError,
    407: CredentialDefinitionAlreadyExistsError,
    500: UnknownCryptoTypeError,
    600: DIDAlreadyExistsError,
    700: UnknownPaymentMethodError,
    701: IncompatiblePaymentMethodsError,
    702: InsufficientFundsError,
    703: PaymentSourceDoesNotExistError,
    704: PaymentOperationNotSupportedError,
    705: ExtraFundsError
}
