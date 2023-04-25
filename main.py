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

import logging
logging.basicConfig(
	format = "[%(levelname)s] %(message)s",
	level = logging.DEBUG
)

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
	ITEM_USE = auto()
	ITEM_INFO = auto()
	INV_VIEW = auto()
	HINT = auto()
	CMD_LIST = auto()
	SAVE = auto()
	LOAD = auto()
	QUIT = auto()

## Log Events
class CustomLogEvent:
	"""A base class for calling log events via the logging module.

	Attributes:
		level: The severity level for this event

		event_type: The name of the event

		event_msg: What the message should be for this event
	"""
	def __init__(self,
				level = logging.INFO,
				event_type = "UnknownEvent",
				event_msg = "An unknown event has occured.") -> None:
		"""Initializes and calls the event

		Args:
			level: The severity level for this event

			event_type: The name of the event

			event_msg: What the message should be for this event
		"""
		self.level = level
		self.event_type = event_type
		self.event_msg = event_msg

		string = f"{self.event_type} - {self.event_msg}"
		match self.level:
			case logging.DEBUG: logging.debug(string)
			case logging.INFO: logging.info(string)
			case logging.WARNING: logging.warning(string)
			case logging.ERROR: logging.error(string)
			case logging.CRITICAL:
				logging.critical(string)
				exit()

class HitWall(CustomLogEvent):
	"""The player hit a wall whilst trying to move"""
	def __init__(self):
		super().__init__(logging.INFO,
						"HitWall",
						"A wall blocks your path.")

class InvalidDirection(CustomLogEvent):
	"""The player somehow moved in a non-cardinal direction"""
	def __init__(self):
		super().__init__(logging.ERROR,
						"InvalidDirection",
						"An invalid direction was passed into Player.move().")

class UnassignedVariable(CustomLogEvent):
	"""The code somehow failed to assign a value to a variable"""
	def __init__(self):
		super().__init__(logging.ERROR,
						"UnassignedVariable",
						"The code didn't assign a value to a variable.")

class UnexpectedTileChar(CustomLogEvent):
	"""There was an unexpected tile character in the area string"""
	def __init__(self):
		super().__init__(logging.ERROR,
						"UnexpectedTileChar",
						"Area could not be created from string")

class InvalidUserInput(CustomLogEvent):
	"""The user did not give a valid input"""
	def __init__(self):
		super().__init__(logging.WARNING,
						"InvalidUserInput",
						"Command was not recognized")

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
	def create_from_str(string: str):
		"""Returns a new area created from a string (this is a temporary
		method)

		Args:
			string: The string to read data from

		Raises:
			UnassignedVariable: The code somehow failed to assign a
			value to a variable

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
					UnexpectedTileChar()

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

	def move(self, direction: Direction, area: Area) -> None:
		"""Try to move the player in a specified direction

		Args:
			direction: The direction the player tries to move in

			area: The area the player is currently in

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
				InvalidDirection()
				return

		new_pos = self.pos + input_vector
		target_tile = area.tiles[new_pos.y][new_pos.x]
		match target_tile.name:
			case "wall": HitWall()
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
				count: int = 1) -> None:
		"""Creates an item, but doesn't put it in the player's inventory

		Args:
			display_name: The name the player will see

			id: The unique item ID used to identify this item

			consumable: Determines whether or not this item's count will
			go down when used

			func: The function to call when used

			count: How many copies of the item the player has
		"""
		self.display_name = display_name
		self.id = id
		self.consumable = consumable
		self.func = func
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

# Functions
def cls():
	"""Clears the terminal"""
	system("cls" if os_name == "nt" else "clear")

def title_screen():
	"""Display the title screen and get the appropriate input

	Raises:
		InvalidUserInput: The user did not give a valid input
	"""
	DISPLAY_TEXT = r"""
 _                   _              _   _____
| |                 | |            | | |_   _|
| |      ___    ___ | | __ ___   __| |   | |  _ __
| |     / _ \  / __|| |/ // _ \ / _` |   | | | '_ \
| |____| (_) || (__ |   <|  __/| (_| |  _| |_| | | |
\_____/ \___/  \___||_|\_\\___| \__,_|  \___/|_| |_|
         A Text Adventure by David Lawrence

                   p > Play Game
                   q > Quit
	"""
	while True:
		print(DISPLAY_TEXT)
		raw_input = input("> ")
		if raw_input == "q": exit()
		elif raw_input == "p": return

		cls()
		InvalidUserInput()

def get_input(): pass

def main() -> None:
	save_file = File()
	title_screen()
	cls()
	save_file.load_files()
	save_file.player.pos = Vector2Int(2, 2)
	save_file.save_files()
	print(save_file.world[0].get_str(save_file.player.pos))

if __name__ == "__main__": main()