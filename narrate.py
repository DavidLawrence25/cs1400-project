# Built-In Libraries
from json import dump, load
from os import remove, get_terminal_size, system
# Custom Libraries
from util import Vector2

# Constants
MAPSIZE = Vector2(3, 3) # the full world map size
COMMENTCHAR = "#"

# Variables
mapCharSet = {
	"player": "☻",
	"item": "✱",
	"wall": "█",
	"passageL": "⇇",
	"passageR": "⇉",
	"passageU": "⇈",
	"passageD": "⇊"
}

map = []
feedback = ""

# Classes
class TilePresets:
	'''The tile presets for building the map.'''
	@staticmethod
	def Air() -> dict:
		return {
			"type": "air",
			"id": "air"
		}
	@staticmethod
	def Player() -> dict:
		return {
			"type": "player",
			"id": "player"
		}
	@staticmethod
	def Item(name: str) -> dict:
		return {
			"type": "item",
			"id": name
		}
	@staticmethod
	def Wall() -> dict:
		return {
			"type": "wall",
			"id": "wall"
		}
	@staticmethod
	def Passage(direction: Vector2) -> dict:
		return {
			"type": "passage",
			"id": direction
		}

# Functions
def GetString(addr: int) -> str:
	'''Return a string from the narration file.'''
	# open the file
	with open("narration.txt", "r") as file:
		# make address strings to check against
		addrStart = f"%{addr}%\n"
		addrEnd = f"%{addr + 1}%\n"
		# get the text
		text = ""
		isReading = False
		for line in file:
			if isReading:
				if line == addrEnd: break
				elif line[0] == COMMENTCHAR: continue
				else: text += line
			if line == addrStart: isReading = True
	return text.strip()

def PlayerlessMap() -> list[list[dict]]:
	'''Return a version of the map without the player.'''
	output = []
	for row in map:
		newRow = [TilePresets.Air() if tile == TilePresets.Player() else tile for tile in row]
		output.append(newRow)
	return output

def LoadMapFromFile(pos: Vector2) -> None:
	'''Loads a room from maps.json into the map variable.'''
	global map
	with open("SaveFile\maps.json", "r") as file: data = load(file)
	map = data[pos.ToIndex(MAPSIZE.x)]

def SaveMapToFile(pos: Vector2) -> None:
	'''Saves the current room to the specified position on the map.'''
	with open(r"SaveFile\maps.json", "r") as file:
		data = load(file)
		data[pos.ToIndex(MAPSIZE.x)] = PlayerlessMap()

	remove(r"SaveFile\maps.json")
	with open(r"SaveFile\maps.json", "w") as file: dump(data, file, indent = "\t")

def GetMapString(map: list[list[dict]]) -> str:
	'''Returns a printable version of the current room.'''
	outputStr = ""
	for row in map:
		for tile in row:
			match tile["type"]:
				case "air": outputStr += " "
				case "player": outputStr += mapCharSet["player"]
				case "item": outputStr += mapCharSet["item"]
				case "wall": outputStr += mapCharSet["wall"]
				case "passage":
					match tile["id"]:
						case "l": outputStr += mapCharSet["passageL"]
						case "r": outputStr += mapCharSet["passageR"]
						case "u": outputStr += mapCharSet["passageU"]
						case "d": outputStr += mapCharSet["passageD"]
		outputStr += "\n"
	return outputStr

def Display(mapStr: str, narration: str, feedback: str) -> None:
	mapLines = mapStr.splitlines(); textLines = feedback.splitlines();
	if feedback != "": textLines.append("")
	for line in narration.splitlines(): textLines.append(line)
	consoleW = get_terminal_size().columns; mapW = len(map[0]); textW = consoleW - mapW
	iterCount = len(mapLines) if len(mapLines) > len(textLines) else len(textLines)
	outputStr = ""
	for i in range(iterCount):
		if len(mapLines) > i and len(textLines) > i: outputStr += f"{textLines[i]:<{textW}}{mapLines[i]}\n"
		elif len(textLines) > i: outputStr += f"{textLines[i]:<{textW}}\n"
		else: outputStr += f"{mapLines[i]:>{consoleW}}\n"
	system("cls"); print(outputStr)