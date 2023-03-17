# Built-In Libraries
from json import load, dumps

# Classes
class ItemFuncs:
	@staticmethod
	def OpenNotepad():
		print("You opened your notepad")
	@staticmethod
	def SlashSword():
		print("You slashed your sword and missed (haha)")

# Constants
ITEMPRESETS = {
	"notepad": {
		"name": "Notepad",
		"count": 1,
		"expendable": False,
		"function": "OpenNotepad"
	},
	"sword": {
		"name": "Sword",
		"count": 1,
		"expendable": True,
		"function": "SlashSword"
	}
}

# Variables
inv = [
	ITEMPRESETS["notepad"],
	ITEMPRESETS["sword"]
]

invNames = [
	"notepad",
	"sword"
]

# Functions
def GetItemStats(name: str) -> dict:
	'''Get the current stats for an item in the inventory.'''
	index = invNames.index(name)
	return inv[index]

def IncreaseItemCount(name: str) -> None:
	'''Adds one to the count of a particular item.'''
	if name in invNames:
		item = GetItemStats(name)
		item["count"] += 1
	else:
		inv.append(ITEMPRESETS[name])
		invNames.append(name)

def DecreaseItemCount(name: str) -> None:
	'''Subtracts one to the count of a particular item.'''
	item = GetItemStats(name)
	item["count"] -= 1
	if item["count"] == 0:
		inv.remove(item)
		invNames.remove(name)

def UseItem(name: str) -> None:
	'''Run the function attached to a particular item.'''
	funcName = ITEMPRESETS[name]["function"]
	func = getattr(ItemFuncs, funcName)
	if ITEMPRESETS[name]["expendable"]: DecreaseItemCount(name)
	func()

def SaveInv() -> None:
	'''Saves the inventory to JSON files.'''
	jsonStr = dumps(inv, indent="\t")
	with open(r"SaveFile\inv.json", "w") as file: file.write(jsonStr)
	jsonStr = dumps(invNames, indent="\t")
	with open(r"SaveFile\invNames.json", "w") as file: file.write(jsonStr)

def LoadInv() -> None:
	'''Load the inventory from JSON files.'''
	global inv, invNames
	with open(r"SaveFile\inv.json", "r") as file: inv = load(file)
	with open(r"SaveFile\invNames.json", "r") as file: invNames = load(file)

def GetInvString() -> str:
	'''Returns a string with all the items in the inventory.'''
	output = "-- INVENTORY --\n"
	for item in invNames:
		displayName = ITEMPRESETS[item]["name"]
		displayCount = ITEMPRESETS[item]["count"]
		output += f"{displayName:<10} | {displayCount:>2}\n"
	return output