import interface
import util

class Tile(object):
	def __init__(self, name: str = "air"):
		self.__name = name

class DirectionalTile(Tile):
	def __init__(self, name: str, direction: str):
		super().__init__(name)
		self.__direction = direction

class Area(object):
	def __init__(self,
				name: str | None = None,
				size: tuple | None = None) -> None:
		self.__name = name if name is not None else "Area"
		self.__size = size if size is not None else (24, 12)
		self.__tiles = util.generate_2d_list(Tile(), self.__size)

class Map(object):
	def __init__(self, size: tuple | None = None) -> None:
		self.__size = size if size is not None else (3, 3)
		self.__tiles = util.generate_2d_list(Area(), self.__size)