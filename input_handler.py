# Built-In Libraries
from enum import Enum
from enum import auto
from json import dumps, loads
# Custom Libraries
import interface
from error_handler import throw_error, ErrorType
import inventory
import narrate

# Classes
class BetterPlayer(interface.Listener):
	def __init__(self, pos: tuple[int]) -> None:
		self.__pos = pos
		#self.subscribe("", )
	
	@property
	def pos(self) -> tuple[int]: return self.__pos

	@pos.setter
	def pos(self, p: tuple[int]) -> None:
		if len(p) != 2: pass #! ERROR
		if type(p[0]) is not int or type(p[1]) is not int: pass #! ERROR

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

class InputHandler(interface.Listener):
	def __init__(self) -> None:
		self.on_input_received = interface.Event("on_input_received")
		self.on_input_parsed = interface.Event("on_input_parsed")

		self.subscribe("on_input_check_passed", self.parse_input)
		self.subscribe("on_input_check_failed", self.get_input)

	def get_input(self) -> None:
		raw_input = input("> ")
		cmd = raw_input.split(" ")[0]
		args = raw_input.split(" ")[1:]
		self.on_input_received(cmd, tuple(args))

	def parse_input(self, cmd, *args) -> None:
		output = tuple()
		match cmd:
			case "w": output = (InputActions.MOVE_UP,)
			case "s": output = (InputActions.MOVE_DOWN,)
			case "a": output = (InputActions.MOVE_LEFT,)
			case "d": output = (InputActions.MOVE_RIGHT,)
			case "move":
				match args[0]:
					case "north" | "n": output = (InputActions.MOVE_UP,)
					case "south" | "s": output = (InputActions.MOVE_DOWN,)
					case "east" | "e": output = (InputActions.MOVE_RIGHT,)
					case "west" | "w": output = (InputActions.MOVE_LEFT,)
			case "use": output = (InputActions.USE_ITEM, *args)
			case "info":output = (InputActions.ITEM_INFO, *args)
			case "inv": output = (InputActions.VIEW_INV,)
			case "help": output = (InputActions.CMD_LIST,)
			case "?": output = (InputActions.HINT,)
			case "file":
				match args[0]:
					case "save" | "s": output = (InputActions.SAVE,)
					case "load" | "l": output = (InputActions.LOAD,)
					case "quit" | "q": output = (InputActions.QUIT,)

		self.on_input_parsed(output)

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
