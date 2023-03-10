import util
import json

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
	]
]

def GetString(addr: int) -> str:
	# open the file
	file = open("narration.txt", "r")
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
	file.close()
	return text.strip()

def GetTile(pos: util.Vector2) -> dict: return map[int(pos.y)][int(pos.x)]