import interface
import util

MAP_CHAR_SET = {
	"air": " ",
	"player": "☻",
	"item": "✱",
	"wall": "█",
	"passageL": "⇇",
	"passageR": "⇉",
	"passageU": "⇈",
	"passageD": "⇊"
}

class Tile(object):
	def __init__(self, name: str = "air"):
		self.__name = name

	@property
	def name(self) -> str: return self.__name

	@name.setter
	def name(self, new_name) -> None:
		if type(new_name) is not str: raise TypeError
		self.__name = new_name

class DirectionalTile(Tile):
	def __init__(self, name: str, direction: str):
		super().__init__(name)
		self.__direction = direction

	@property
	def direction(self) -> str: return self.__direction

	@direction.setter
	def direction(self, new_direction) -> None:
		if type(new_direction) is not str: raise TypeError
		if new_direction not in ("n", "s", "e", "w"): raise ValueError
		self.__direction = new_direction

class Area(interface.Listener):
	def __init__(self, name: str = "Area", size: tuple = (24, 12)) -> None:
		self.__name = name
		self.__size = size
		self.__tiles = util.generate_2d_list(Tile(), self.__size)

		self.on_get_tile = interface.Event("on_get_tile")

		self.subscribe("on_try_move", self.get_tile)

	def __str__(self) -> str:
		string = f"{self.__name}\n\n"
		for row in self.__tiles:
			for tile in row:
				match tile.name:
					case "passage":
						match tile.direction:
							case "n": string += MAP_CHAR_SET["passageU"]
							case "s": string += MAP_CHAR_SET["passageD"]
							case "e": string += MAP_CHAR_SET["passageR"]
							case "w": string += MAP_CHAR_SET["passageL"]
					case _: string += MAP_CHAR_SET[tile.name]
			string += "\n"
		return string

	def get_tile(self, pos: util.Vector2Int, property: str = ""):
		tile = self.__tiles[pos.y][pos.x]
		return_val = None
		match property:
			case "name": return_val = tile.name
			case "direction":
				if type(tile) is DirectionalTile: return_val = tile.direction
				else: raise AttributeError
			case _: return_val = tile

		self.on_get_tile(pos, return_val)

	def playerless(self):
		new_map = self.__tiles
		for row in new_map:
			for tile in row:
				if tile.name == "player": tile = "air"
		return new_map

class Map(object):
	def __init__(self, size: tuple | None = None) -> None:
		self.__size = size if size is not None else (3, 3)
		self.__tiles = util.generate_2d_list(Area(), self.__size)