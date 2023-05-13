# Modules
## Built-In
from enum import Enum, auto
from pathlib import Path
from os import system
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

		get_from_user(): Returns a Vector2Int based on the user's input
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
		"""Asks for a vector from the user and tries to create one with
		the information provided until it succeeds."""
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
	CMD_LIST = auto()
	SAVE = auto()
	LOAD = auto()
	QUIT = auto()

class ItemAction(Enum):
	USE = auto()
	INFO = auto()

## Log Events
class Logger:
	"""I made a logger because the logging module didn't work for my
	purposes

	Class Constants:
		DEBUG = "DEBUG"

		INFO = "INFO"

		WARNING = "WARNING"

		ERROR = "ERROR"

		CRITICAL = "CRITICAL"

	Methods:
		format_message(event_type, msg, level): Produces a log message
		from the name of the event, the message, and the level of
		severity associated with that event
	"""

	DEBUG = "DEBUG"
	INFO = "INFO"
	WARNING = "WARNING"
	ERROR = "ERROR"
	CRITICAL = "CRITICAL"

	def __init__(self): return None

	@staticmethod
	def format_message(event_type: str, msg: str, level: str) -> str:
		"""Produces a log message as a string

		Args:
			event_type: The name of the event

			msg: The message associated with that event

			level: How serious the event is
		"""
		return f"[{level}] {event_type} - {msg}"

class CustomLogEvent:
	"""A base class for calling log events

	Attributes:
		level: The severity level for this event

		event_type: The name of the event

		event_msg: What the message should be for this event
	"""

	def __init__(self): return None

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

def log_hit_wall():
	"""The player hit a wall whilst trying to move"""

	return CustomLogEvent.call(Logger.INFO,
								"HitWall",
								"A wall blocks your path")

def log_invalid_direction():
	"""The player somehow moved in a non-cardinal direction"""

	return CustomLogEvent.call(Logger.ERROR,
								"InvalidDirection",
								"An invalid direction was passed into move")

def log_unassigned_variable():
	"""The code somehow failed to assign a value to a variable"""

	return CustomLogEvent.call(Logger.CRITICAL,
								"UnassignedVariable",
								"The code didn't assign a value to a variable")

def log_unexpected_tile_char():
	"""There was an unexpected tile character in the area string"""

	return CustomLogEvent.call(Logger.CRITICAL,
								"UnexpectedTileChar",
								"Area could not be created from string")

def log_invalid_user_input():
	"""The user did not give a valid input"""

	return CustomLogEvent.call(Logger.WARNING,
								"InvalidUserInput",
								"Command was not recognized")

def log_item_not_found():
	"""The item specified doesn't exist in the player's inventory"""

	return CustomLogEvent.call(Logger.WARNING,
								"ItemNotFound",
								"That item isn't in your inventory")

def log_unsaved_progress():
	"""There is unsaved progress that may be erased"""

	return CustomLogEvent.call(Logger.WARNING,
								"UnsavedProgress",
								"You have unsaved progress. Are you sure?")

def log_get_item(item_name: str):
	"""The player collected an item

	Args:
		item_name: The name of the item the player just got
	"""

	return CustomLogEvent.call(Logger.INFO,
								"GetItem",
								f"You collected a {item_name}!")

def log_wrong_room():
	"""The player tried to use an item in the wrong area"""

	return CustomLogEvent.call(Logger.WARNING,
								"WrongRoom",
								"You can't use that item here")

def log_incorrect_combination():
	"""The player entered an incorrect combination"""

	return CustomLogEvent.call(Logger.INFO,
								"IncorrectCombination",
								"That was the wrong combination")

def log_not_an_int(thing: str):
	"""The code tried to cast a variable to an int, but couldn't

	Args:
		thing: The user-friendly name of the variable in question
	"""

	return CustomLogEvent.call(Logger.ERROR,
								"NotAnInt",
								f"{thing.title()} must be an integer")

def log_incorrect_combination_length():
	"""The combination was not 10 digits long"""

	return CustomLogEvent.call(Logger.ERROR,
								"IncorrectCombinationLength",
								"Combination must be 10 digits long")

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
				direction: Direction | None = None,
				appearance: str = "") -> None:
		"""Creates a tile object

		Args:
			name: The name of the tile used by the code to identify it

			id: This specifies which item the tile represents, if any

			direction: The direction a passage tile points

			appearance: An alternate string to display instead of the
			default specified in the Area class' CHARSET constant
		"""
		self.name = name
		self.id = id
		self.direction = direction
		self.appearance = appearance

	@staticmethod
	def air(): return Tile("air")

	@staticmethod
	def item(id: str): return Tile("item", id = id)

	@staticmethod
	def wall(): return Tile("wall")

	@staticmethod
	def wall_2(): return Tile("wall", appearance="▒▒")

	@staticmethod
	def passage(direction: Direction):
		return Tile("passage", direction = direction)

	@staticmethod
	def fake_wall():
		return Tile("passage", appearance="██")

	@staticmethod
	def lock(direction: Direction):
		return Tile("lock", direction = direction)

class Area:
	"""A detailed 2D array of tiles

	Attributes:
		name: The name of the area

		pos: The position of the area in the map

		size: The dimensions of the area measured in tiles

		tiles: A 2D array of tiles

		passages: A list of passage-passage-area tuples

		narration_address: Which address to load from when in this area

	Class Constants:
		CHARSET: A set of characters to represent all possible tiles

	Methods:
		matching_passage(tile_pos): Returns the matching passage in
		another area for a given tile in this area

		get_str(player_pos): Returns a string representation of the area

		create_from_str(string): Returns a new area created from a
		string (this is a temporary method)
	"""

	CHARSET = {
		"air": "  ",
		"player": ":)",
		"item": "()",
		"wall": "██",
		"lockNS": "==",
		"lockEW": "||",
		"passageL": "🡀🡀",
		"passageR": "🡂🡂",
		"passageU": "⬆⬆",
		"passageD": "⬇⬇"
	}

	def __init__(self,
				name: str,
				pos: Vector2Int,
				size: Vector2Int,
				narration_address: int) -> None:
		"""Creates an area object filled with air tiles

		Args:
			name: The name of the area

			pos: The position of the area in the map

			size: The dimensions of the area measured in tiles

			narration_address: Which address to load from when in this
			area
		"""
		self.name = name
		self.pos = pos
		self.size = size
		self.narration_address = narration_address
		self.tiles = []
		self.passages = []

	def matching_passage(self, tile_pos: Vector2Int) -> list:
		"""Returns the matching passage in another area for a given tile
		in this area

		Args:
			tile_pos: The position of the passage in this area
		"""
		matches = [pair for pair in self.passages if pair[0] == tile_pos]
		return matches[0][1:]

	def get_str(self, player_pos: Vector2Int) -> str:
		"""Gets the string representation of the area

		Args:
			player_pos: The position of the player in the current area
		"""
		output = ""
		for y, row in enumerate(self.tiles):
			for x, tile in enumerate(row):
				if Vector2Int(x, y) == player_pos:
					output += Area.CHARSET["player"]
				elif tile.appearance != "":
					output += tile.appearance
				elif tile.name == "passage":
					if tile.direction == Direction.NORTH:
						output += Area.CHARSET["passageU"]
					elif tile.direction == Direction.SOUTH:
						output += Area.CHARSET["passageD"]
					elif tile.direction == Direction.EAST:
						output += Area.CHARSET["passageR"]
					elif tile.direction == Direction.WEST:
						output += Area.CHARSET["passageL"]
				elif tile.name == "lock":
					if tile.direction in (Direction.NORTH, Direction.SOUTH):
						output += Area.CHARSET["lockNS"]
					else: # east & west
						output += Area.CHARSET["lockEW"]
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
		narration_address = int(input("Enter narration index > "))
		result = Area(name, pos, size, narration_address)
		for y, line in enumerate(lines):
			result.tiles.append([])
			for x, tile in enumerate(line):
				if tile == "A":
					result.tiles[y].append(Tile.air())
				elif tile == "I":
					id = input("Enter item id > ")
					result.tiles[y].append(Tile.item(id))
				elif tile == "W":
					result.tiles[y].append(Tile.wall())
				elif tile == "?":
					result.tiles[y].append(Tile.fake_wall())
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				elif tile == "O":
					result.tiles[y].append(Tile.wall_2())
				elif tile == "L":
					result.tiles[y].append(Tile.lock(Direction.NORTH))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				elif tile == "l":
					result.tiles[y].append(Tile.lock(Direction.SOUTH))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				elif tile == ")":
					result.tiles[y].append(Tile.lock(Direction.EAST))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
				elif tile == "(":
					result.tiles[y].append(Tile.lock(Direction.WEST))
					result.passages.append(
						Area.generate_passage_pair(Vector2Int(x, y))
					)
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
					narrator.feedback = log_unexpected_tile_char()

		return result

class Player:
	"""A simple player object that can move around the map

	Attributes:
		pos: The coordinates of the player in the current area relative
		to the top-left corner (0, 0)

		area_pos: The coordinates of the current area in the world map
		relative to the top-left corner (0, 0)

		inventory: A list containing all the items the player has

	Methods:
		move(direction, area): Try to move the player in a specified
		direction
	"""

	def __init__(self, pos: Vector2Int, area_pos: Vector2Int) -> None:
		"""Initializes the instance with a position, current area,
		and inventory

		Args:
			pos: The coordinates of the player in the current area
			relative to the top-left corner (0, 0)

			area_pos: The coordinates of the current area in the world
			map relative to the top-left corner (0, 0)
		"""
		self.pos = pos
		self.area_pos = area_pos
		self.inventory = []

	def move(self, direction: Direction, area: Area, file, narrator) -> None:
		"""Try to move the player in a specified direction

		Args:
			direction: The direction the player tries to move in

			area: The area the player is currently in

			file: The currently-loaded save file

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
				narrator.feedback = log_invalid_direction()
				return

		new_pos = self.pos + input_vector
		if new_pos.y in range(10) and new_pos.x in range(10):
			target_tile = area.tiles[new_pos.y][new_pos.x]
		else:
			narrator.feedback = log_hit_wall()
			return
		if target_tile.name in ("wall", "lock"):
			narrator.feedback = log_hit_wall()
		else:
			this_area = file.world[area_pos_to_index(self.area_pos)]
			if target_tile.name == "passage":
				new_pos, self.area_pos = this_area.matching_passage(new_pos)
			elif target_tile.name == "item":
				item_preset = ALL_ITEMS[target_tile.id]
				matches = []
				for i, item in enumerate(self.inventory):
					if item.id == target_tile.id:
						matches.append(item)
						matches.append(i)
						break
				if len(matches) != 0:
					current_item, index = matches
					current_item.count += 1
					self.inventory[index] = current_item
				else:
					self.inventory.append(item_preset)

				narrator.feedback = log_get_item(item_preset.display_name)
				this_area.tiles[new_pos.y][new_pos.x] = Tile.air()

			self.pos = new_pos

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

	def increment_count(self, file, step: int = 1) -> None:
		"""Adds a set amount to the count, deleting the item instance if
		it drops below 1

		Args:
			file: The currently-loaded save file

			step: The amount to increment the count by
		"""
		self.count += step
		if self.count < 1: file.player.inventory.remove(self)

	def use(self, file, narrator) -> None:
		"""Call func and decrement count if the item is consumable

		Args:
			file: The currently-loaded save file

			narrator: The unique narrator instance
		"""
		self.func(file, narrator)
		if self.consumable: self.increment_count(file, -1)

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

	def save_files(self, narrator) -> None:
		"""Saves data from this instance to the SaveFile directory"""
		self.save_file("world")
		self.save_file("player")
		narrator.feedback = "[INFO] File saved successfully"

	def save_file(self, name: str) -> None:
		with open(str(SAVE_FILE_PATHS[name]), "wb") as file:
			pickle.dump(self.__getattribute__(name), file)

class Narrator:
	"""A simple narrator that stores all of the complex narration code

	Attributes:
		map: A string representation of the current area

		narration: The most recent string retrieved from narration.txt

		feedback: The message from the most recent logging event

	Class Constants:
		COMMENT_CHAR: The character for comments in narration.txt

	Methods:
		get_narration(addr): Returns a string from the narration file

		get_inventory(player): Get a string representation of the
		player's inventory

		cls(): Clears the terminal

		display(file): Displays the information for a given file state
	"""

	COMMENT_CHAR = "#"

	def __init__(self) -> None:
		"""Creates a narrator (this should be the only instance)"""
		self.map: str = ""
		self.__feedback: str = ""
		self.has_updated_feedback: bool = False

	@property
	def feedback(self) -> str:
		return self.__feedback

	@feedback.setter
	def feedback(self, new: str) -> None:
		if type(new) is str:
			self.__feedback = new
			self.has_updated_feedback = True
		else: raise TypeError

	@staticmethod
	def get_narration(addr: int) -> str:
		"""Return a string from the narration file

		Args:
			addr: The address of the narration in narration.txt
		"""
		with open("narration.txt", "r") as file:
			addr_start = f"%{addr}%\n"
			addr_end = f"%{addr + 1}%\n"
			text = ""
			is_reading = False
			for line in file:
				if is_reading:
					if line == addr_end: break
					elif line[0] == Narrator.COMMENT_CHAR: continue
					else: text += line
				if line == addr_start: is_reading = True
		return text[:len(text) - 1]

	@staticmethod
	def get_inventory(player: Player) -> str:
		"""Get a string representation of the player's inventory

		Args:
			player: The player object
		"""
		inventory = player.inventory
		output = "----- INVENTORY -----\n"
		for item in inventory:
			output += f"{item.display_name:<16} | {item.count:>2}\n"
		return output.strip()

	@staticmethod
	def cls() -> None:
		"""Clears the terminal"""
		system("cls" if os_name == "nt" else "clear")

	def display(self, file: File) -> None:
		"""Displays the information for a given file state

		Args:
			file: The currently-loaded save file
		"""
		area = file.world[area_pos_to_index(file.player.area_pos)]
		area_str = area.get_str(file.player.pos)
		narration = Narrator.get_narration(area.narration_address)
		Narrator.cls()
		if self.has_updated_feedback:
			print(f"""-- {area.name} --

{area_str}
{self.feedback}
----------------
{narration}""")
		else:
			print(f"""-- {area.name} --

{area_str}

{narration}""")
		self.has_updated_feedback = False

# Functions
## Utilities
def title_screen(narrator: Narrator):
	"""Display the title screen and get the appropriate input

	Args:
		narrator: The unique narrator instance

	Raises:
		InvalidUserInput: The user did not give a valid input
	"""
	DISPLAY_TEXT = Narrator.get_narration(2)
	while True:
		print(DISPLAY_TEXT)
		raw_input = input("> ")
		if raw_input == "q": exit()
		elif raw_input == "p": return

		narrator.feedback = log_invalid_user_input()

def area_pos_to_index(pos: Vector2Int) -> int:
	"""Converts an area's position to its index in the world

	Args:
		pos: The area's position

	Raises:
		ValueError: Inappropriate argument value (of correct type)

		TypeError: Inappropriate argument type
	"""
	if pos == Vector2Int(0, 0): return 0
	elif pos == Vector2Int(1, 0): return 1
	elif pos == Vector2Int(2, 0): return 2
	elif pos == Vector2Int(3, 0): return 3
	elif pos == Vector2Int(4, 0): return 4
	elif pos == Vector2Int(5, 0): return 5
	elif pos == Vector2Int(0, 1): return 6
	elif pos == Vector2Int(2, 1): return 7
	elif pos == Vector2Int(3, 1): return 8
	elif pos == Vector2Int(4, 1): return 9
	elif type(pos) is Vector2Int: raise ValueError
	else: raise TypeError

def get_input(narrator: Narrator) -> tuple:
	"""Get and process an input from the user

	Args:
		narrator: The unique narrator instance

	Raises:
		InvalidUserInput: The user did not give a valid input
	"""
	raw_input = input("> ")
	cmd = raw_input.split(" ")[0]
	args = raw_input.split(" ")[1:]
	match cmd:
		case "w": return (UserInput.MOVE, Direction.NORTH)
		case "s": return (UserInput.MOVE, Direction.SOUTH)
		case "a": return (UserInput.MOVE, Direction.WEST)
		case "d": return (UserInput.MOVE, Direction.EAST)
		case "move":
			if len(args) > 0:
				match args[0]:
					case "north" | "n": return (UserInput.MOVE, Direction.NORTH)
					case "south" | "s": return (UserInput.MOVE, Direction.SOUTH)
					case "east" | "e": return (UserInput.MOVE, Direction.EAST)
					case "west" | "w": return (UserInput.MOVE, Direction.WEST)
		case "use": return (UserInput.ITEM, ItemAction.USE, *args)
		case "info": return (UserInput.ITEM, ItemAction.INFO, *args)
		case "inv": return (UserInput.INV_VIEW,)
		case "help": return (UserInput.CMD_LIST,)
		case "file":
			if len(args) > 0:
				match args[0]:
					case "save" | "s": return (UserInput.SAVE,)
					case "load" | "l": return (UserInput.LOAD,)
					case "quit" | "q": return (UserInput.QUIT,)

	narrator.feedback = log_invalid_user_input()
	return ()

def call_func_from_input(user_input: tuple,
						file: File,
						narrator: Narrator,
						is_progress_saved: bool) -> bool:
	"""Calls a function based on the input, returns whether or not the
	player's progress is saved.

	Args:
		user_input: The result of the get_input() function

		file: The currently-loaded save file

		narrator: The unique narrator instance

		is_progress_saved: A flag that checks whether or not the player
		is safe to quit the file without saving beforehand

	Raises:
		UnsavedProgress: There is unsaved progress that may be erased
	"""
	if len(user_input) == 0: return is_progress_saved
	match user_input[0]:
		case UserInput.MOVE:
			file.player.move(
				user_input[1],
				file.world[area_pos_to_index(file.player.area_pos)],
				file,
				narrator
			)
			return False
		case UserInput.ITEM:
			item = None
			has_found_item = False
			for item in file.player.inventory:
				try:
					if item.id == user_input[2]:
						item = item
						has_found_item = True
						break
				except:
					continue
			if not has_found_item:
				narrator.feedback = log_item_not_found()
				return is_progress_saved
			if item is None:
				narrator.feedback = log_unassigned_variable()
				return is_progress_saved
			elif user_input[1] == ItemAction.USE:
				item.use(file, narrator)
			elif user_input[1] == ItemAction.INFO:
				narrator.feedback = Narrator.get_narration(item.info_address)
		case UserInput.INV_VIEW:
			narrator.feedback = Narrator.get_inventory(file.player)
		case UserInput.CMD_LIST:
			narrator.feedback = Narrator.get_narration(1)
		case UserInput.SAVE:
			file.save_files(narrator)
		case UserInput.LOAD:
			should_quit = False
			if not is_progress_saved:
				confirmation = ""
				while confirmation not in ("y", "yes", "n", "no"):
					confirmation = input(f"{log_unsaved_progress()} > ")
				should_quit = "y" in confirmation
			else:
				should_quit = True
			if should_quit: file.load_files()
		case UserInput.QUIT:
			should_quit = False
			if not is_progress_saved:
				confirmation = ""
				while confirmation not in ("y", "yes", "n", "no"):
					confirmation = input(f"{log_unsaved_progress()} > ")
				should_quit = "y" in confirmation
			else:
				should_quit = True
			if should_quit: exit()
	return user_input[0] in (UserInput.MOVE, UserInput.ITEM, UserInput.SAVE) \
	and is_progress_saved

## Item Functions
def solve_cube(file: File, narrator: Narrator):
	narrator.feedback = narrator.get_narration(14)
	file.player.inventory.append(ALL_ITEMS["paper_strip"])

def print_e(file: File, narrator: Narrator):
	math_poster = ALL_ITEMS["math_poster"]
	if math_poster in file.player.inventory \
	and file.player.area_pos == Vector2Int(0, 1):
		response = ""
		while response not in ("yes", "y", "no", "n"):
			response = input("Do you understand now? > ")
		if "y" in response:
			response = input("What is the door combination? > ")
			try:
				guess = int(response)
			except ValueError:
				narrator.feedback = log_not_an_int("combination")
				return
			if len(response.strip()) != 10:
				narrator.feedback = log_incorrect_combination_length()
			elif guess != 2718281828:
				narrator.feedback = log_incorrect_combination()
			else:
				file.world[6].tiles[4][9].name = "passage"
				file.world[7].tiles[4][0].name = "passage"
				narrator.feedback = "[INFO] You successfully unlocked the door"
		else:
			narrator.feedback = "[INFO] Oh, ok. Take your time ;)"
	else:
		narrator.feedback = narrator.get_narration(16)

def look_at_framed_paper(file: File, narrator: Narrator):
	narrator.feedback = narrator.get_narration(18)

def unlock_front_door(file: File, narrator: Narrator):
	VALID_COLORS = (
		"red",
		"orange",
		"yellow",
		"green",
		"blue",
		"purple",
		"pink",
		"white",
		"black"
	)
	correct_colors = {"green", "white", "orange"}
	correct_numbers = {4, 7, 9, 2, 3}
	correct_guesses = 0

	has_asked = False
	for _ in range(3):
		guess = ""
		while guess not in VALID_COLORS:
			if has_asked: print("[WARNING] That isn't a standard color")
			guess = input("Name a color based on the items you've seen\n> ").lower()
			if guess in correct_colors:
				correct_guesses += 1
				correct_colors.remove(guess)
			has_asked = True

	has_asked = False
	for _ in range(5):
		guess = 11
		while guess not in range(10):
			if has_asked: print("[WARNING] The number must be between 0 & 9")
			guess = int(input("Name a number based on the items you've seen\n> "))
			if guess in correct_numbers:
				correct_guesses += 1
				correct_numbers.remove(guess)
			has_asked = True

	if correct_guesses != 8:
		narrator.feedback = log_incorrect_combination()
		return

	if file.player.area_pos == Vector2Int(4, 1):
		file.world[10].tiles[9][3].name = "passage"
		file.world[10].tiles[9][4].name = "passage"
		file.world[10].tiles[9][5].name = "passage"
		file.world[10].tiles[9][6].name = "passage"
		narrator.feedback = narrator.get_narration(20)
	else:
		narrator.feedback = log_wrong_room()

def read_poster(file: File, narrator: Narrator):
	math_poster = ALL_ITEMS["paper_strip"]
	if math_poster in file.player.inventory \
	and file.player.area_pos == Vector2Int(0, 1):
		response = ""
		while response not in ("yes", "y", "no", "n"):
			response = input("Do you understand now? > ")
		if "y" in response:
			response = input("What is the door combination? > ")
			try:
				guess = int(response)
			except ValueError:
				narrator.feedback = log_not_an_int("combination")
				return
			if len(response.strip()) != 10:
				narrator.feedback = log_incorrect_combination_length()
			elif guess != 2718281828:
				narrator.feedback = log_incorrect_combination()
			else:
				file.world[6].tiles[4][9].name = "passage"
				file.world[7].tiles[4][0].name = "passage"
				narrator.feedback = "[INFO] You successfully unlocked the door"
		else:
			narrator.feedback = "[INFO] Oh, ok. Take your time ;)"
	else:
		narrator.feedback = narrator.get_narration(22)

ALL_ITEMS = {
	"rubiks_cube": Item("Rubik's Cube", "rubiks_cube", True, solve_cube, 13),
	"paper_strip": Item("Paper Strip", "paper_strip", False, print_e, 15),
	"framed_paper": Item("Framed Paper", "framed_paper", False, look_at_framed_paper, 17),
	"house_key": Item("House Key", "house_key", True, unlock_front_door, 19),
	"math_poster": Item("Math Poster", "math_poster", False, read_poster, 21)
}

## Main
def main() -> None:
	save_file = File()
	narrator = Narrator()
	is_progress_saved = True

	Narrator.cls()
	title_screen(narrator)
	save_file.load_files()

	narrator.display(save_file)
	while True:
		user_input = get_input(narrator)
		is_progress_saved = call_func_from_input(user_input,
												save_file,
												narrator,
												is_progress_saved)
		narrator.display(save_file)

if __name__ == "__main__": main()