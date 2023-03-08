mapCharSet = {
	"player": "🯅",
	"item": "🯄",
	"wall": "🮿",
	"passageL": "🮵",
	"passageR": "🮶",
	"passageU": "🮸",
	"passageD": "🮷",
	"arrowL": "◀",
	"arrowR": "▶",
	"arrowU": "▲",
	"arrowD": "▼"
}

COMMENTCHAR = "#"

def getString(addr: int) -> str:
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