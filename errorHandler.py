from enum import Enum
from enum import auto

class ErrorType(Enum):
	INITVARTYPE = auto(),
	UNKNOWNCMD = auto(),
	NUMOFARGS = auto(),
	INVALIDARG = auto()

def ThrowError(errorType: ErrorType, info: list) -> str:
	match errorType:
		case ErrorType.INITVARTYPE: return f"Tried to initialize variable {info[0]} with type {info[1]}, expected {info[2]}"
		case ErrorType.UNKNOWNCMD: return f"Input {info[0]} is not a valid command"
		case ErrorType.NUMOFARGS:
			pluralMod = ""
			if info[1] != 1: pluralMod = "s"
			return f"Command {info[0]} got {info[1]} argument{pluralMod}, expected {info[2]}"
		case ErrorType.INVALIDARG:
			return f"Argument {info[0]} is not valid for the command {info[1]}"
		case _: return "Error thrown without an error type"