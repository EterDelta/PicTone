class SamplerError(Exception):
    """Base exception raised for all sampler related errors."""
    pass


class InvalidThresholdError(SamplerError):
    """Raised when an invalid edge threshold is passed to the sampler"""

    def __init__(self, threshold: int):
        error_message = f"Invalid edge detection threshold: {threshold}. Threshold must be between 0 and 255"
        super().__init__(error_message)


class UnsupportedDepthError(SamplerError):
    """Raised when an unsupported depth is used by the sampler"""

    def __init__(self, bit_depth: int):
        error_message = f"Unsupported bit depth: {bit_depth}"
        super().__init__(error_message)
