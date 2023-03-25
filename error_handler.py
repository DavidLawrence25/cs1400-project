# Built-In Libraries
from enum import Enum
from enum import auto
# Custom Libraries
import interface

# Classes
class ErrorType(Enum):
	INIT_VAR_TYPE = auto(),
	UNKNOWN_CMD = auto(),
	NUM_OF_ARGS = auto(),
	INVALID_ARG = auto()

class ErrorHandler(interface.Listener):
	def __init__(self) -> None: pass

class InputEH(ErrorHandler):
	VALID_CMDS = (
		"w",
		"s",
		"a",
		"d",
		"move",
		"use",
		"info",
		"inv",
		"help",
		"?",
		"file"
	)

	NUM_OF_EXPECTED_ARGS = {
		"w": 0,
		"s": 0,
		"a": 0,
		"d": 0,
		"move": 1,
		"use": 1,
		"info": 1,
		"inv": 0,
		"help": 0,
		"?": 0,
		"file": 1
	}

	possible_args = {
		"move": ["north", "south", "east", "west", "n", "s", "e", "w"],
		"use": inventory.ITEM_PRESETS,
		"file": ["save", "load", "quit", "s", "l", "q"]
	}

	def __init__(self) -> None:
		self.on_input_check_passed = interface.Event("on_input_check_passed")
		self.on_input_check_failed = interface.Event("on_input_check_failed")
		self.on_inv_ids_requested = interface.Event("on_inv_ids_requested")

		self.subscribe("on_input_received", self.check_input)
		self.subscribe("on_inv_ids_fetched", self.update_inv_ids)

	@staticmethod
	def update_inv_ids(inv_ids: list) -> None:
		InputEH.possible_args["info"] = inv_ids

	def check_input(self, cmd, *args) -> None:
		has_thrown_error = False
		if not cmd in InputEH.VALID_CMDS:
			has_thrown_error = True #! ERROR
		if len(args) != InputEH.NUM_OF_EXPECTED_ARGS[cmd]:
			has_thrown_error = True #! ERROR
		if cmd == "info":
			self.on_inv_ids_requested()
		try:
			if args[0] not in InputEH.possible_args[cmd]:
				has_thrown_error = True #! ERROR
		except IndexError: pass

		if has_thrown_error: self.on_input_check_failed()
		else: self.on_input_check_passed(cmd, args)

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