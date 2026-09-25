"""Typed errors for FDSE domain and trust-boundary failures."""


class FDSEError(Exception):
    """Base class for expected FDSE failures."""


class ConfigurationError(FDSEError):
    """Raised when configuration is missing or invalid."""


class BoundaryViolation(FDSEError):
    """Raised when FDSE attempts an operation outside an allowed boundary."""


class ContractViolation(FDSEError):
    """Raised when an integration contract is malformed or unsupported."""
