import json
import errorHandler

class Item:
	def __init__(self, name: str, count: int, expendable: bool, function: str):
		if type(name) is str: self.name = name
		else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{name=}".split("=")[0], type(name), str]))
		if type(count) is int: self.count = count
		else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{count=}".split("=")[0], type(count), int]))
		if type(expendable) is bool: self.expendable = expendable
		else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{expendable=}".split("=")[0], type(expendable), bool]))
		if type(function) is str: self.function = function
		else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{function=}".split("=")[0], type(function), str]))

class ItemFuncs:
	def OpenNotepad():
		print("You opened your notepad")
	def SlashSword():
		print("You slashed your sword and missed (haha)")

allItems = {
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

inv = [
	allItems["notepad"],
	allItems["sword"]
]

invNames = [
	"notepad",
	"sword"
]

def ObtainItem(name: str) -> None:
	inv.append(allItems[name])
	invNames.append(name)

def DropItem(name: str) -> None:
	index = invNames.index(name)
	inv[index]["count"] -= 1
	if inv[index]["count"] == 0:
		del inv[index]
		invNames.remove("name")

def UseItem(name: str) -> None:
	funcName = allItems[name]["function"]
	func = getattr(ItemFuncs, funcName)
	func()

def SaveInv() -> None:
	jsonStr = json.dumps(inv, indent="\t")
	file = open("inv.json", "w")
	file.write(jsonStr)
	file.close()