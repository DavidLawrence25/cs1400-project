# Built-In Libraries
from enum import Enum
from enum import auto

# Classes
class ErrorType(Enum):
	INIT_VAR_TYPE = auto(),
	UNKNOWN_CMD = auto(),
	NUM_OF_ARGS = auto(),
	INVALID_ARG = auto()

# Functions
def throw_error(error_type: ErrorType, info: list) -> str:
	match error_type:
		case ErrorType.INIT_VAR_TYPE: return f"Tried to initialize variable {info[0]} with type {info[1]}, expected {info[2]}"
		case ErrorType.UNKNOWN_CMD: return f"Input {info[0]} is not a valid command"
		case ErrorType.NUM_OF_ARGS:
			plural_mod = "" if info[1] == 1 else "s"
			return f"Command {info[0]} got {info[1]} argument{plural_mod}, expected {info[2]}"
		case ErrorType.INVALID_ARG:
			return f"Argument {info[0]} is not valid for the command {info[1]}"
		case _: return "Error thrown without an error type"