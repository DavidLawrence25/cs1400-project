# Built-In Libraries
from enum import Enum
from enum import auto
from json import dumps, loads
# Custom Libraries
from error_handler import throw_error, ErrorType
from util import Vector2
import inventory
import narrate

# Classes
class Player:
	'''A player object.'''
	def __init__(self, pos: Vector2) -> None:
		self.pos = pos
	def __str__(self) -> str: return f"Player Object at {self.pos}"
	def to_dict(self) -> dict:
		'''Returns the player as a dictionary.'''
		json_str = dumps(self, default=lambda o: o.__dict__, indent="\t")
		return loads(json_str)
	@staticmethod
	def from_dict(obj: dict):
		'''Returns an instance of the player from a dictionary.'''
		return Player(Vector2.from_dict(obj["pos"]))

	def place_in_map(self) -> None:
		'''Places the player in the room based on their current position.'''
		narrate.map[self.pos.y][self.pos.x] = narrate.TilePresets.player()
	def move(self, direction: str) -> None:
		'''Moves the player in the given direction if possible.'''
		match direction:
			case "l": input_vector = Vector2.west()
			case "r": input_vector = Vector2.east()
			case "u": input_vector = Vector2.north()
			case "d": input_vector = Vector2.south()
			case _: raise ValueError(throw_error(ErrorType.INVALID_ARG, [direction, "move"]))
		new_pos = Vector2.add(self.pos, input_vector)
		new_tile = narrate.map[new_pos.y][new_pos.x]
		match new_tile["type"]:
			case "wall":
				narrate.feedback = "A wall stands in your path."
				return
			case "passage":
				# room changing crap
				return
			case "item": inventory.increase_item_count(new_tile["id"])
		# this code will only run if the new tile was air or an item
		narrate.map[self.pos.y][self.pos.x] = narrate.TilePresets.air()
		narrate.map[new_pos.y][new_pos.x] = narrate.TilePresets.player()
		self.pos = new_pos

class InputActions(Enum):
	'''An enumeration of all possible actions the player can take.'''
	MOVE_UP = auto(),
	MOVE_DOWN = auto(),
	MOVE_LEFT = auto(),
	MOVE_RIGHT = auto(),
	USE_ITEM = auto(),
	ITEM_INFO = auto(),
	VIEW_INV = auto(),
	HINT = auto(),
	CMD_LIST = auto(),
	SAVE = auto(),
	LOAD = auto(),
	QUIT = auto()

# Constants
MUTABLE_ACTIONS = (
	InputActions.MOVE_UP,
	InputActions.MOVE_DOWN,
	InputActions.MOVE_LEFT,
	InputActions.MOVE_RIGHT,
	InputActions.USE_ITEM,
)

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

# Variables
possible_args = {
	"move": ["north", "south", "east", "west", "n", "s", "e", "w"],
	"use": inventory.ITEM_PRESETS,
	"info": inventory.inv_names,
	"file": ["save", "load", "quit", "s", "l", "q"]
}

# Functions
def update_inv_items() -> None:
	'''Updates the possible arguments for the "info" command to match what is inside the inventory.'''
	possible_args["info"] = inventory.inv_names

def get_input() -> list:
	'''Get an input from the player and returns a list with the input action and argument(s).'''
	cmd = ""; args = []
	# loop until the input is valid
	while True:
		# get the raw input
		raw_input = input("> ")
		# split the input into a command and the arguments
		cmd = raw_input.split(" ")[0]; args = raw_input.split(" ")[1:]
		# throw an error if the command isn't valid
		if not cmd in VALID_CMDS:
			print(throw_error(ErrorType.UNKNOWN_CMD, [cmd]))
			continue
		# throw an error if the number of arguments isn't right
		if len(args) != NUM_OF_EXPECTED_ARGS[cmd]:
			print(throw_error(ErrorType.NUM_OF_ARGS, [cmd, len(args), NUM_OF_EXPECTED_ARGS[cmd]]))
			continue
		# update the possible arguments for the info command if needed
		if cmd == "info": update_inv_items()
		# throw an error if the argument is not valid
		try:
			if args[0] not in possible_args[cmd]:
				print(throw_error(ErrorType.INVALID_ARG, [args[0], cmd]))
				continue
		except IndexError: pass

		# return the corresponding stuff
		match cmd:
			case "w": return [InputActions.MOVE_UP, ""]
			case "s": return [InputActions.MOVE_DOWN, ""]
			case "a": return [InputActions.MOVE_LEFT, ""]
			case "d": return [InputActions.MOVE_RIGHT, ""]
			case "move":
				match args[0]:
					case "north" | "n": return [InputActions.MOVE_UP, ""]
					case "south" | "s": return [InputActions.MOVE_DOWN, ""]
					case "east" | "e": return [InputActions.MOVE_RIGHT, ""]
					case "west" | "w": return [InputActions.MOVE_LEFT, ""]
			case "use": return [InputActions.USE_ITEM, args[0]]
			case "info": return [InputActions.ITEM_INFO, args[0]]
			case "inv": return [InputActions.VIEW_INV, ""]
			case "help": return [InputActions.CMD_LIST, ""]
			case "?": return [InputActions.HINT, ""]
			case "file":
				match args[0]:
					case "save" | "s": return [InputActions.SAVE, ""]
					case "load" | "l": return [InputActions.LOAD, ""]
					case "quit" | "q": return [InputActions.QUIT, ""]