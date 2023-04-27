# Modules
## Built-In
from enum import Enum, auto
from pathlib import Path
from os import system, get_terminal_size
from os import name as os_name
import pickle

APP_ROOT = Path(".")
SAVE_FILE_PATHS = {
	"world": APP_ROOT / "SaveFile" / "world.pkl",
	"player": APP_ROOT / "SaveFile" / "player.pkl"
}
DEFAULT_FILE_PATHS = {
	"world": APP_ROOT / "DefaultSaveData" / "world.pkl",
	"player": APP_ROOT / "DefaultSaveData" / "player.pkl"
}

# Classes
## Utilities
class Vector2Int:
	"""A simplistic vector of two integers.

	Attributes:
		x: An integer describing the horizontal component of the vector

		y: An integer describing the vertical component of the vector

	Methods:
		zero(): Returns (0, 0)

		up(): Returns (0, 1)

		down(): Returns (0, -1)

		left(): Returns (-1, 0)

		right(): Returns (1, 0)
	"""

	def __init__(self, x: int, y: int) -> None:
		"""Initializes the instance with x and y components.

		Args:
			x: An integer describing the horizontal component of the
			vector

			y: An integer describing the vertical component of the
			vector
		"""
		self.__x = x
		self.__y = y

	@property
	def x(self) -> int: return self.__x

	@x.setter
	def x(self, new_x: int) -> None:
		if type(new_x) is int: self.__x = new_x
		else: raise TypeError

	@property
	def y(self) -> int: return self.__y

	@y.setter
	def y(self, new_y: int | float) -> None:
		if type(new_y) is int: self.__y = new_y
		else: raise TypeError

	def __eq__(self, vector) -> bool:
		if self.__x == vector.x and self.__y == vector.y:
			return True
		else:
			return False

	def __add__(self, vector):
		return Vector2Int(self.__x + vector.x, self.__y + vector.y)

	def __sub__(self, vector):
		return Vector2Int(self.__x - vector.x, self.__y - vector.y)

	def __iadd__(self, vector):
		self = self + vector
		return self

	def __isub__(self, vector):
		self = self - vector
		return self

	def __str__(self) -> str:
		return f"<{self.x}, {self.y}>"

	@staticmethod
	def zero(): return Vector2Int(0, 0)

	@staticmethod
	def up(): return Vector2Int(0, 1)

	@staticmethod
	def down(): return Vector2Int(0, -1)

	@staticmethod
	def left(): return Vector2Int(-1, 0)

	@staticmethod
	def right(): return Vector2Int(1, 0)

	@staticmethod
	def get_from_user():
		is_valid = False
		vector = Vector2Int.zero()
		while not is_valid:
			vector_raw = input("Enter Vector2Int > ")
			vector_raw = vector_raw.replace(" ", "")
			vector_raw = vector_raw.split(",")
			if len(vector_raw) == 2:
				vector = Vector2Int(int(vector_raw[0]), int(vector_raw[1]))
				is_valid = True
		return vector

## Enums
class Direction(Enum):
	"""A cardinal direction

	Attributes:
		NORTH

		SOUTH

		EAST

		WEST
	"""
	NORTH = auto()
	SOUTH = auto()
	EAST = auto()
	WEST = auto()

class UserInput(Enum):
	"""A code derived from user input to call the correct function

	Attributes:
		MOVE: Move in a given direction

		ITEM_USE: Use an item

		ITEM_INFO: Display info about an item

		INV_VIEW: Display the inventory

		HINT: Give the player a hint about what to do next

		CMD_LIST: List all possible commands

		SAVE: Save the file

		LOAD: Load the file

		QUIT: Quit the game
	"""
	MOVE = auto()
	ITEM = auto()
	INV_VIEW = auto()
	HINT = auto()
	CMD_LIST = auto()
	SAVE = auto()
	LOAD = auto()
	QUIT = auto()

class ItemAction(Enum):
	USE = auto()
	INFO = auto()

## Log Events
class Logger:
	""""""

	DEBUG = "DEBUG"
	INFO = "INFO"
	WARNING = "WARNING"
	ERROR = "ERROR"
	CRITICAL = "CRITICAL"

	@staticmethod
	def format_message(event_type: str, msg: str, level: str) -> str:
		return f"[{level}] {event_type} - {msg}"

class CustomLogEvent:
	"""A base class for calling log events

	Attributes:
		level: The severity level for this event

		event_type: The name of the event

		event_msg: What the message should be for this event
	"""

	@staticmethod
	def call(level = Logger.INFO,
			event_type = "UnknownEvent",
			event_msg = "An unknown event has occured.") -> str:
		"""Makes a string for this event, calling it if it's critical

		Args:
			level: The severity level for this event

			event_type: The name of the event

			event_msg: What the message should be for this event
		"""
		string = Logger.format_message(event_type, event_msg, level)
		if level is Logger.CRITICAL:
			print(string)
			exit()
		return string

class HitWall(CustomLogEvent):
	"""The player hit a wall whilst trying to move"""

	@staticmethod
	def call():
		return super().call(Logger.INFO,
							"HitWall",
							"A wall blocks your path")

class InvalidDirection(CustomLogEvent):
	"""The player somehow moved in a non-cardinal direction"""

	@staticmethod
	def call():
		return super().call(Logger.ERROR,
							"InvalidDirection",
							"An invalid direction was passed into move")

class UnassignedVariable(CustomLogEvent):
	"""The code somehow failed to assign a value to a variable"""

	@staticmethod
	def call():
		return super().call(Logger.CRITICAL,
							"UnassignedVariable",
							"The code didn't assign a value to a variable")

class UnexpectedTileChar(CustomLogEvent):
	"""There was an unexpected tile character in the area string"""

	@staticmethod
	def call():
		return super().call(Logger.CRITICAL,
							"UnexpectedTileChar",
							"Area could not be created from string")

class InvalidUserInput(CustomLogEvent):
	"""The user did not give a valid input"""

	@staticmethod
	def call():
		return super().call(Logger.WARNING,
							"InvalidUserInput",
							"Command was not recognized")

class ItemNotFound(CustomLogEvent):
	"""The item specified doesn't exist in the player's inventory"""

	@staticmethod
	def call():
		return super().call(Logger.WARNING,
							"ItemNotFound",
							"That item isn't in your inventory")

class UnsavedProgress(CustomLogEvent):
	"""There is unsaved progress that may be erased"""

	@staticmethod
	def call():
		return super().call(Logger.WARNING,
							"UnsavedProgress",
							"You have unsaved progress. Are you sure?")

## Main
class Tile:
	"""A basic tile meant to be stored inside an Area's tiles array

	Attributes:
		name: The name of the tile's type (item, wall, passage, etc.)

		id: A specific identifier used for special tiles like items

		direction: The direction a passage is pointing in

	Methods:
		air(): Returns an air tile

		item(id): Returns an item tile with the specified ID

		wall(): Returns a wall tile

		passage(direction): Returns a passage pointing in the specified
		direction
	"""
	def __init__(self,
				name: str = "",
				id: str = "",
				direction: Direction | None = None) -> None:
		self.name = name
		self.id = id
		self.direction = direction

	@staticmethod
	def air(): return Tile("air")

	@staticmethod
	def item(id: str): return Tile("item", id = id)

	@staticmethod
	def wall(): return Tile("wall")

	@staticmethod
	def passage(direction: Direction):
		return Tile("passage", direction = direction)

class Area:
	"""A detailed 2D array of tiles

	Attributes:
		name: The name of the area

		pos: The position of the area in the map

		size: The dimensions of the area measured in tiles

		tiles: A 2D array of tiles

		passages: A list of passage-passage-area tuples

	Methods:
		matching_passage(tile_pos): Returns the matching passage in
		another area for a given tile in this area

		create_from_str(string): Returns a new area created from a
		string (this is a temporary method)
	"""

	CHARSET = {
		"air": "  ",
		"player": ":)",
		"item": "()",
		"wall": "██",
		"passageL": "🡀🡀",
		"passageR": "🡂🡂",
		"passageU": "⬆⬆",
		"passageD": "⬇⬇"
	}

	def __init__(self, name: str, pos: Vector2Int, size: Vector2Int) -> None:
		"""Creates an area object filled with air tiles

		Args:
			name: The name of the area

			pos: The position of the area in the map

			size: The dimensions of the area measured in tiles
		"""
		self.name = name
		self.pos = pos
		self.size = size
		self.tiles = []
		self.passages = [] # [(passage_a, passage_b, that_area)]

	def matching_passage(self, tile_pos: Vector2Int) -> list:
		"""Returns the matching passage in another area for a given tile
		in this area

		Args:
			tile_pos: The position of the passage in this area
		"""
		matches = [pair for pair in self.passages if pair[0] == tile_pos]
		return matches[0][1:]

	def get_str(self, player_pos: Vector2Int) -> str:
		output = ""
		for y, row in enumerate(self.tiles):
			for x, tile in enumerate(row):
				if Vector2Int(x, y) == player_pos:
					output += Area.CHARSET["player"]
				elif tile.name == "passage":
					if tile.direction == Direction.NORTH:
						output += Area.CHARSET["passageU"]
					elif tile.direction == Direction.SOUTH:
						output += Area.CHARSET["passageD"]
					elif tile.direction == Direction.EAST:
						output += Area.CHARSET["passageR"]
					else: # west
						output += Area.CHARSET["passageL"]
				else:
					output += Area.CHARSET[tile.name]
			output += "\n"
		return output

	@staticmethod
	def generate_passage_pair(tile_pos_0: Vector2Int) -> tuple:
		print(f"Passage detected at {tile_pos_0}")
		print("Please provide the position of the matching passage")
		tile_pos_1 = Vector2Int.get_from_user()
		print("Please provide the position of the area this passage maps to")
		area_pos = Vector2Int.get_from_user()
		return (tile_pos_0, tile_pos_1, area_pos)

	@staticmethod
	def create_from_str(string: str, narrator):
		"""Returns a new area created from a string (this is a temporary
		method)

		Args:
			string: The string to read data from
			narrator: The instance of the Narrator class

		Raises:
			UnexpectedTileChar: There was an unexpected tile character
			in the area string
		"""
		lines = string.splitlines()
		size = Vector2Int(len(lines[0]), len(lines))
		name = input("Enter name > ")
		pos = Vector2Int.get_from_user()
		result = Area(name, pos, size)
		for y, line in enumerate(lines):
			result.tiles.append([])
			for x, tile in enumerate(line):
				if tile == " ":
					result.tiles[y].append(Tile.air())
				elif tile == "I":
					id = input("Enter item id > ")
					result.tiles[y].append(Tile.item(id))
				elif tile == "W":
					result.tiles[y].append(Tile.wall())
				elif tile == "^":
					result.tiles[y].append(Tile.passage(Direction.NORTH))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				elif tile == "v":
					result.tiles[y].append(Tile.passage(Direction.SOUTH))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				elif tile == ">":
					result.tiles[y].append(Tile.passage(Direction.EAST))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				elif tile == "<":
					result.tiles[y].append(Tile.passage(Direction.WEST))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				else:
					narrator.feedback = UnexpectedTileChar.call()

		return result

class Player:
	"""A simple player object that can move around the map

	Attributes:
		pos: The coordinates of the player in the current area relative
		to the top-left corner (0, 0)

		area: The coordinates of the current area in the world map
		relative to the top-left corner (0, 0)

		inventory: A list containing all the items the player has

	Methods:
		move(direction, area): Try to move the player in a specified
		direction

		change_room(new_area_pos): ???
	"""

	def __init__(self, pos: Vector2Int, area_pos: Vector2Int) -> None:
		"""Initializes the instance with a position, current area,
		and inventory

		Args:
			pos: The coordinates of the player in the current area
			relative to the top-left corner (0, 0)

			area: The coordinates of the current area in the world map
			relative to the top-left corner (0, 0)
		"""
		self.pos = pos
		self.area_pos = area_pos
		self.inventory = []

	def move(self, direction: Direction, area: Area, narrator) -> None:
		"""Try to move the player in a specified direction

		Args:
			direction: The direction the player tries to move in

			area: The area the player is currently in

			narrator: The instance of the Narrator class

		Raises:
			InvalidDirection: direction wasn't in the Direction enum

			HitWall: The tile the player tried to walk into was a wall
		"""
		match direction:
			case Direction.NORTH: input_vector = Vector2Int.down()
			case Direction.SOUTH: input_vector = Vector2Int.up()
			case Direction.EAST: input_vector = Vector2Int.right()
			case Direction.WEST: input_vector = Vector2Int.left()
			case _:
				narrator.feedback = InvalidDirection.call()
				return

		new_pos = self.pos + input_vector
		target_tile = area.tiles[new_pos.y][new_pos.x]
		match target_tile.name:
			case "wall": narrator.feedback = HitWall.call()
			case "passage":
				pass # TODO: create a function to move between rooms
			case "item":
				pass # TODO: create a function to pick up items
			case _: self.pos = new_pos

	def change_room(self, new_area_pos: Vector2Int) -> None:
		pass

class Item:
	"""An item inside the player's inventory

	Attributes:
		display_name: The name the player will see

		id: The unique item ID used to identify this item

		consumable: Determines whether or not this item's count will go
		down when used

		func: The function to call when used

		info_address: The address of the info text in narration.txt

		count: How many copies of the item the player has

	Methods:
		increment_count(step): Adds a set amount to the count, deleting
		the item instance if it drops below 1

		use(): Call func and decrement count if the item is consumable
	"""

	def __init__(self,
				display_name: str,
				id: str,
				consumable: bool,
				func,
				info_address: int,
				count: int = 1) -> None:
		"""Creates an item, but doesn't put it in the player's inventory

		Args:
			display_name: The name the player will see

			id: The unique item ID used to identify this item

			consumable: Determines whether or not this item's count will
			go down when used

			func: The function to call when used

			info_address: The address of the info text in narration.txt

			count: How many copies of the item the player has
		"""
		self.display_name = display_name
		self.id = id
		self.consumable = consumable
		self.func = func
		self.info_address = info_address
		self.count = count

	def increment_count(self, step: int = 1) -> None:
		"""Adds a set amount to the count, deleting the item instance if
		it drops below 1

		Args:
			step: The amount to increment the count by
		"""
		self.count += step
		if self.count < 1: del self

	def use(self) -> None:
		"""Call func and decrement count if the item is consumable"""
		self.func()
		if self.consumable: self.increment_count(-1)

class File:
	"""A save file pulled from the SaveFile directory

	Attributes:
		world: A 2D array of areas

		player: An instance of the Player class

	Methods:
		load_files(): Loads data from the appropriate directory into
		this instance

		save_files(): Saves data from this instance to the SaveFile
		directory
	"""

	def __init__(self) -> None:
		"""Instantiates an empty file object"""
		self.world = []
		self.player = Player(Vector2Int.zero(), Vector2Int.zero())

	def load_files(self) -> None:
		"""Loads data from the appropriate directory into this
		instance"""
		self.load_file("world")
		self.load_file("player")

	def load_file(self, name: str) -> None:
		if SAVE_FILE_PATHS[name].is_file():
			read_location = str(SAVE_FILE_PATHS[name])
		else:
			read_location = str(DEFAULT_FILE_PATHS[name])

		with open(read_location, "rb") as file:
			if name == "world": self.world = pickle.load(file)
			elif name == "player": self.player = pickle.load(file)

	def save_files(self) -> None:
		"""Saves data from this instance to the SaveFile directory"""
		self.save_file("world")
		self.save_file("player")

	def save_file(self, name: str) -> None:
		with open(str(SAVE_FILE_PATHS[name]), "wb") as file:
			pickle.dump(self.__getattribute__(name), file)

class Narrator:
	"""A simple narrator that stores all of the complex narration code

	Attributes:
		map: A string representation of the current area

		narration: The most recent string retrieved from narration.txt

		feedback: The message from the most recent logging event

	Constants:
		COMMENT_CHAR: The character for comments in narration.txt

	Methods:
		get_string(addr): Returns a string from the narration file
	"""

	COMMENT_CHAR = "#"

	def __init__(self) -> None:
		self.map: str = ""
		self.narration: str = ""
		self.feedback: str = ""

	@staticmethod
	def get_narration(addr: int) -> str:
		"""Return a string from the narration file"""
		# open the file
		with open("narration.txt", "r") as file:
			# make address strings to check against
			addr_start = f"%{addr}%\n"
			addr_end = f"%{addr + 1}%\n"
			# get the text
			text = ""
			is_reading = False
			for line in file:
				if is_reading:
					if line == addr_end: break
					elif line[0] == Narrator.COMMENT_CHAR: continue
					else: text += line
				if line == addr_start: is_reading = True
		return text.strip()

	@staticmethod
	def get_inventory(player: Player) -> str:
		inventory = player.inventory
		output = "-- INVENTORY --\n"
		for item in inventory:
			output += f"{item.display_name:<10} | {item.count:>2}\n"
		return output

	@staticmethod
	def cls() -> None:
		"""Clears the terminal"""
		system("cls" if os_name == "nt" else "clear")

	@staticmethod
	def display(map_str: str, narration: str, feedback: str) -> None:
		map_lines = map_str.splitlines()
		text_lines = feedback.splitlines()
		if feedback != "": text_lines.append("")
		text_lines.append(*narration.splitlines())
		terminal_w = get_terminal_size().columns
		map_w = len(map_lines[0])
		text_w = terminal_w - map_w
		if len(map_lines) > len(text_lines):
			iter_count = len(map_lines)
		else:
			iter_count = len(text_lines)

		output = ""
		for i in range(iter_count):
			if len(map_lines) > i and len(text_lines) > i:
				output += f"{text_lines[i]:<{text_w}}{map_lines[i]}\n"
			elif len(text_lines) > i:
				output += f"{text_lines[i]:<{text_w}}\n"
			else:
				output += f"{map_lines[i]:>{terminal_w}}\n"

		Narrator.cls()
		print(output)

# Functions
def title_screen(narrator: Narrator):
	"""Display the title screen and get the appropriate input

	Raises:
		InvalidUserInput: The user did not give a valid input
	"""
	DISPLAY_TEXT = Narrator.get_narration(2)
	while True:
		print(DISPLAY_TEXT)
		raw_input = input("> ")
		if raw_input == "q": exit()
		elif raw_input == "p": return

		narrator.feedback = InvalidUserInput.call()

def area_pos_to_index(pos: Vector2Int) -> int:
	match pos:
		case Vector2Int(0, 0): return 0
		case Vector2Int(1, 0): return 1
		case Vector2Int(2, 0): return 2
		case Vector2Int(3, 0): return 3
		case Vector2Int(0, -1): return 4
		case Vector2Int(1, -1): return 5
		case Vector2Int(2, -1): return 6
		case Vector2Int(3, -1): return 7
		case _:
			if type(pos) is Vector2Int: raise ValueError
			else: raise TypeError

def get_input() -> tuple:
	raw_input = input("> ")
	cmd = raw_input.split(" ")[0]
	args = raw_input.split(" ")[1:]
	match cmd:
		case "w": return (UserInput.MOVE, Direction.NORTH)
		case "s": return (UserInput.MOVE, Direction.SOUTH)
		case "a": return (UserInput.MOVE, Direction.WEST)
		case "d": return (UserInput.MOVE, Direction.EAST)
		case "move":
			match args[0]:
				case "north" | "n": return (UserInput.MOVE, Direction.NORTH)
				case "south" | "s": return (UserInput.MOVE, Direction.SOUTH)
				case "east" | "e": return (UserInput.MOVE, Direction.EAST)
				case "west" | "w": return (UserInput.MOVE, Direction.WEST)
		case "use": return (UserInput.ITEM, ItemAction.USE, *args[1:])
		case "info": return (UserInput.ITEM, ItemAction.INFO, *args[1:])
		case "inv": return (UserInput.INV_VIEW,)
		case "help": return (UserInput.CMD_LIST,)
		case "?": return (UserInput.HINT,)
		case "file":
			match args[0]:
				case "save" | "s": return (UserInput.SAVE,)
				case "load" | "l": return (UserInput.LOAD,)
				case "quit" | "q": return (UserInput.QUIT,)

	InvalidUserInput()
	return ()

def call_func_from_input(user_input: tuple,
						file: File,
						narrator: Narrator,
						is_progress_saved: bool) -> bool:
	"""Calls a function based on the input, returns whether or not the
	player's progress is saved."""
	match user_input[0]:
		case UserInput.MOVE:
			file.player.move(
				user_input[1],
				file.world[area_pos_to_index(file.player.area_pos)],
				narrator
			)
		case UserInput.ITEM:
			item = None
			has_found_item = False
			for item in file.player.inventory:
				if item.id == user_input[2]:
					item = item
					has_found_item = True
					break
			if not has_found_item:
				ItemNotFound()
				return
			if item is None:
				UnassignedVariable()
				return
			elif user_input[1] == ItemAction.USE:
				item.use()
			elif user_input[1] == ItemAction.INFO:
				narrator.feedback = Narrator.get_narration(item.info_address)
		case UserInput.INV_VIEW:
			narrator.feedback = Narrator.get_inventory(file.player)
		case UserInput.CMD_LIST:
			narrator.feedback = Narrator.get_narration(1)
		case UserInput.HINT:
			pass
			#???
		case UserInput.SAVE:
			file.save_files()
		case UserInput.LOAD:
			should_quit = False
			if not is_progress_saved:
				confirmation = ""
				while confirmation not in ("y", "yes", "n", "no"):
					confirmation = input(f"{UnsavedProgress()} > ")
				should_quit = "y" in confirmation
			else:
				should_quit = True
			if should_quit: file.load_files()
		case UserInput.QUIT:
			should_quit = False
			if not is_progress_saved:
				confirmation = ""
				while confirmation not in ("y", "yes", "n", "no"):
					confirmation = input(f"{UnsavedProgress()} > ")
				should_quit = "y" in confirmation
			else:
				should_quit = True
			if should_quit: exit()
	return user_input[0] in (UserInput.MOVE, UserInput.ITEM)

def main() -> None:
	save_file = File()
	narrator = Narrator()
	is_progress_saved = True
	title_screen(narrator)
	Narrator.cls()
	save_file.load_files()
	save_file.player.pos = Vector2Int(2, 2)
	save_file.save_files()
	print(save_file.world[0].get_str(save_file.player.pos))
	print(get_input())

if __name__ == "__main__": main()