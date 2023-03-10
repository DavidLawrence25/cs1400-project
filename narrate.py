import util
import json
import os

mapCharSet = {
	"player": "☻",
	"item": "✱",
	"wall": "█",
	"passageL": "⇇",
	"passageR": "⇉",
	"passageU": "⇈",
	"passageD": "⇊",
	"arrowL": "◀",
	"arrowR": "▶",
	"arrowU": "▲",
	"arrowD": "▼"
}

COMMENTCHAR = "#"

class TilePresets:
	@staticmethod
	def Air() -> dict:
		return {
			"type": "air",
			"id": "air"
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
	def Passage(direction: util.Vector2) -> dict:
		return {
			"type": "passage",
			"id": direction
		}
	@staticmethod
	def Arrow(direction: util.Vector2) -> dict:
		return {
			"type": "arrow",
			"id": direction
		}

map = [
	[
		TilePresets.Air(),
		TilePresets.Air(),
		TilePresets.Air(),
		TilePresets.Air(),
		TilePresets.Wall(),
		TilePresets.Wall(),
		TilePresets.Wall(),
		TilePresets.Wall(),
		TilePresets.Air(),
		TilePresets.Air()
	],
	10, # width
	11 # height
]

def GetString(addr: int) -> str:
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

def LoadMapFromFile(pos: util.Vector2) -> list[list[dict]]:
	with open("maps.json", "r") as file:
		data = json.load(file)
		# map = data[pos.ToIndex()]

def SaveMapToFile(pos: util.Vector2) -> None:
	with open("maps.json", "r") as file:
		data = json.load(file)
		data[pos.ToIndex(map[-2])] = map
	
	os.remove("maps.json")
	with open("maps.json", "w") as file: json.dump(data, file, indent = "\t")

def GetTile(pos: util.Vector2) -> dict: return map[int(pos.y)][int(pos.x)]