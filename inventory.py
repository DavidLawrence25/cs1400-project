# Built-In Libraries
from json import load, dumps

# Classes
class ItemFuncs:
	@staticmethod
	def open_notepad():
		print("You opened your notepad")
	@staticmethod
	def slash_sword():
		print("You slashed your sword and missed (haha)")

# Constants
ITEM_PRESETS = {
	"notepad": {
		"name": "Notepad",
		"count": 1,
		"expendable": False,
		"function": "open_notepad"
	},
	"sword": {
		"name": "Sword",
		"count": 1,
		"expendable": True,
		"function": "slash_sword"
	}
}

# Variables
inv = [
	ITEM_PRESETS["notepad"],
	ITEM_PRESETS["sword"]
]

inv_names = [
	"notepad",
	"sword"
]

# Functions
def get_item_stats(name: str) -> dict:
	'''Get the current stats for an item in the inventory.'''
	index = inv_names.index(name)
	return inv[index]

def increase_item_count(name: str) -> None:
	'''Adds one to the count of a particular item.'''
	if name in inv_names:
		item = get_item_stats(name)
		item["count"] += 1
	else:
		inv.append(ITEM_PRESETS[name])
		inv_names.append(name)

def decrease_item_count(name: str) -> None:
	'''Subtracts one to the count of a particular item.'''
	item = get_item_stats(name)
	item["count"] -= 1
	if item["count"] == 0:
		inv.remove(item)
		inv_names.remove(name)

def use_item(name: str) -> None:
	'''Run the function attached to a particular item.'''
	func_name = ITEM_PRESETS[name]["function"]
	func = getattr(ItemFuncs, func_name)
	if ITEM_PRESETS[name]["expendable"]: decrease_item_count(name)
	func()

def save_inv() -> None:
	'''Saves the inventory to JSON files.'''
	inv_data = dumps(inv, indent="\t")
	with open(r"SaveFile\inv.json", "w") as file: file.write(inv_data)
	inv_names_data = dumps(inv_names, indent="\t")
	with open(r"SaveFile\inv_names.json", "w") as file: file.write(inv_names_data)

def load_inv() -> None:
	'''Load the inventory from JSON files.'''
	global inv, inv_names
	with open(r"SaveFile\inv.json", "r") as file: inv = load(file)
	with open(r"SaveFile\inv_names.json", "r") as file: inv_names = load(file)

def get_inv_string() -> str:
	'''Returns a string with all the items in the inventory.'''
	output = "-- INVENTORY --\n"
	for item in inv_names:
		name = ITEM_PRESETS[item]["name"]
		count = ITEM_PRESETS[item]["count"]
		output += f"{name:<10} | {count:>2}\n"
	return output