# Modules
## Built-In
from enum import Enum, auto

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
	"""

	def __init__(self, x: int, y: int) -> None:
		"""Initializes the instance with x and y components.

		Args:
			x: An integer describing the horizontal component of the vector
			y: An integer describing the vertical component of the vector
		"""
		self.__x = x
		self.__y = y

	@property
	def x(self) -> int: return self.__x

	@x.setter
	def x(self, new_x: int) -> None:
		if type(new_x) is int: self.__x = new_x
		else: pass #! ERROR

	@property
	def y(self) -> int: return self.__y

	@y.setter
	def y(self, new_y: int | float) -> None:
		if type(new_y) is int: self.__y = new_y
		else: pass #! ERROR

	def __eq__(self, vector) -> bool:
		return self.__x == vector.x and self.__y == vector.y

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

## Enums
class Direction(Enum):
	NORTH = auto()
	SOUTH = auto()
	EAST = auto()
	WEST = auto()

## Log Events
class CustomLogEvent:
	def __init__(self,
				level = logging.INFO,
				event_type = "UnknownEvent",
				event_msg = "An unknown event has occured.") -> None:
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
	def __init__(self):
		super().__init__(logging.INFO,
						"HitWall",
						"A wall blocks your path.")

class InvalidDirection(CustomLogEvent):
	def __init__(self):
		super().__init__(logging.ERROR,
						"InvalidDirection",
						"An invalid direction was passed into Player.move().")

## Main
class Tile:
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
	def __init__(self, name: str, pos: Vector2Int, size: Vector2Int) -> None:
		self.name = name
		self.pos = pos
		self.size = size
		self.tiles = [[Tile.air() for _ in range(size.x)] * size.y]

class Player:
	"""A simple player object that can move around the map.

	Attributes:
		pos: The coordinates of the player in the current area relative
		to the top-left corner. (0, 0)
		area: The coordinates of the current area in the world map
		relative to the top-left corner. (0, 0)
	"""

	def __init__(self, pos: Vector2Int, area_pos: Vector2Int) -> None:
		"""Initializes the instance with a position and current area.

		Args:
			pos: The coordinates of the player in the current area relative
			to the top-left corner. (0, 0)
			area: The coordinates of the current area in the world map
			relative to the top-left corner. (0, 0)
		"""
		self.pos = pos
		self.area_pos = area_pos

	def move(self, direction: Direction, area: Area) -> None:
		"""Try to move the player in a specified direction.

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

class Item:
	def __init__(self,
				display_name: str,
				id: str,
				consumable: bool,
				func,
				count: int = 1) -> None:
		self.display_name = display_name
		self.id = id
		self.consumable = consumable
		self.func = func
		self.count = count

	def increment_count(self, step: int = 1) -> None:
		self.count += step
		if self.count == 0: del self

	def use(self) -> None:
		self.func()
		self.increment_count(-1)