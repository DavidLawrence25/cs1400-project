import util

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

def GetMapString(pos: util.Vector2) -> str:
	# open the file
	file = open("maps.txt", "r")
	# make address strings to check against
	addrStart = f"s%{pos.x},{pos.y}%\n"
	addrEnd = f"e%{pos.x},{pos.y}%\n"
	# get the text
	text = ""
	isReading = False
	for line in file:
		if isReading:
			if line == addrEnd: break
			elif line[0] == COMMENTCHAR: continue
			for char in line:
				match char:
					case "a": text += mapCharSet["player"]
					case "b": text += mapCharSet["item"]
					case "c": text += mapCharSet["wall"]
					case "d": text += mapCharSet["passageL"]
					case "e": text += mapCharSet["passageR"]
					case "f": text += mapCharSet["passageU"]
					case "g": text += mapCharSet["passageD"]
					case "h": text += mapCharSet["arrowL"]
					case "i": text += mapCharSet["arrowR"]
					case "j": text += mapCharSet["arrowU"]
					case "k": text += mapCharSet["arrowD"]
					case "-": text += " "
			text += "\n"
		if line == addrStart: isReading = True
	file.close()
	return text[:len(text) - 2]

def ParseMapString(string: str) -> list:
	lines = string.split("\n")
	ls = [util.CharsFromStr(line) for line in lines]
	return ls[:len(ls) - 1]