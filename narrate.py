# Built-In Libraries
from json import dump, load
from os import remove, get_terminal_size, system
# Custom Libraries
from util import Vector2

# Constants
MAP_SIZE = Vector2(3, 3) # the full world map size
COMMENT_CHAR = "#"
MAP_CHAR_SET = {
	"player": "☻",
	"item": "✱",
	"wall": "█",
	"passageL": "⇇",
	"passageR": "⇉",
	"passageU": "⇈",
	"passageD": "⇊"
}

# Variables
map = []
feedback = ""

# Classes
class TilePresets:
	'''The tile presets for building the map.'''
	@staticmethod
	def air() -> dict:
		return {
			"type": "air",
			"id": "air"
		}
	@staticmethod
	def player() -> dict:
		return {
			"type": "player",
			"id": "player"
		}
	@staticmethod
	def item(name: str) -> dict:
		return {
			"type": "item",
			"id": name
		}
	@staticmethod
	def wall() -> dict:
		return {
			"type": "wall",
			"id": "wall"
		}
	@staticmethod
	def passage(direction: Vector2) -> dict:
		return {
			"type": "passage",
			"id": direction
		}

# Functions
def get_string(addr: int) -> str:
	'''Return a string from the narration file.'''
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
				elif line[0] == COMMENT_CHAR: continue
				else: text += line
			if line == addr_start: is_reading = True
	return text.strip()

def playerless_map() -> list[list[dict]]:
	'''Return a version of the map without the player.'''
	output = []
	for row in map:
		new_row = [TilePresets.air() if tile == TilePresets.player() else tile for tile in row]
		output.append(new_row)
	return output

def load_map_from_file(pos: Vector2) -> None:
	'''Loads a room from maps.json into the map variable.'''
	global map
	with open("SaveFile\maps.json", "r") as file: map_data = load(file)
	map = map_data[pos.to_index(MAP_SIZE.x)]

def save_map_to_file(pos: Vector2) -> None:
	'''Saves the current room to the specified position on the map.'''
	with open(r"SaveFile\maps.json", "r") as file:
		map_data = load(file)
		map_data[pos.to_index(MAP_SIZE.x)] = playerless_map()

	remove(r"SaveFile\maps.json")
	with open(r"SaveFile\maps.json", "w") as file: dump(map_data, file, indent = "\t")

def get_map_string(map: list[list[dict]]) -> str:
	'''Returns a printable version of the current room.'''
	output = ""
	for row in map:
		for tile in row:
			match tile["type"]:
				case "air": output += " "
				case "player": output += MAP_CHAR_SET["player"]
				case "item": output += MAP_CHAR_SET["item"]
				case "wall": output += MAP_CHAR_SET["wall"]
				case "passage":
					match tile["id"]:
						case "l": output += MAP_CHAR_SET["passageL"]
						case "r": output += MAP_CHAR_SET["passageR"]
						case "u": output += MAP_CHAR_SET["passageU"]
						case "d": output += MAP_CHAR_SET["passageD"]
		output += "\n"
	return output

def display(map_str: str, narration: str, feedback: str) -> None:
	map_lines = map_str.splitlines(); text_lines = feedback.splitlines();
	if feedback != "": text_lines.append("")
	text_lines.append(*narration.splitlines())
	terminal_w = get_terminal_size().columns; map_w = len(map[0]); text_w = terminal_w - map_w
	iter_count = len(map_lines) if len(map_lines) > len(text_lines) else len(text_lines)
	output = ""
	for i in range(iter_count):
		if len(map_lines) > i and len(text_lines) > i: output += f"{text_lines[i]:<{text_w}}{map_lines[i]}\n"
		elif len(text_lines) > i: output += f"{text_lines[i]:<{text_w}}\n"
		else: output += f"{map_lines[i]:>{terminal_w}}\n"
	system("cls"); print(output)