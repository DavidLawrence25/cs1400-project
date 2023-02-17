from enum import Enum
from enum import auto

class ErrorType(Enum):
    INITVARTYPE = auto()

def throwError(errorType: ErrorType, info: list) -> str:
    match errorType:
        case ErrorType.INITVARTYPE: return f"Tried to initialize variable {info[0]} with type {info[1]}, expected {info[2]}"
        case _: return "Error thrown without an error type"