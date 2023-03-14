from enum import Enum
from enum import auto
import errorHandler
import inventory
import util

class Player:
	def __init__(self, pos: util.Vector2) -> None:
		self.pos = pos
	def __str__(self) -> str: return f"Player Object at {self.pos}"

	def Move(self, direction: str) -> None:
		match direction:
			case "l": inputVector = util.Vector2.Left()
			case "r": inputVector = util.Vector2.Right()
			case "u": inputVector = util.Vector2.Up()
			case "d": inputVector = util.Vector2.Down()
			case _: raise ValueError(errorHandler.ThrowError(errorHandler.ErrorType.INVALIDARG, [direction, "move"]))
		self.pos = util.Vector2.Add(self.pos, inputVector)

class InputActions(Enum):
	MOVEUP = auto(),
	MOVEDOWN = auto(),
	MOVELEFT = auto(),
	MOVERIGHT = auto(),
	USEITEM = auto(),
	ITEMINFO = auto(),
	VIEWINV = auto(),
	HINT = auto(),
	CMDLIST = auto(),
	SAVE = auto(),
	LOAD = auto(),
	QUIT = auto()

cmdList = [
	"move",
	"use",
	"info",
	"inv",
	"help",
	"?",
	"file"
]

ExpectedArgs = {
	"move": 1,
	"use": 1,
	"info": 1,
	"inv": 0,
	"help": 0,
	"?": 0,
	"file": 1
}

PossibleArgs = {
	"move": ["north", "south", "east", "west", "n", "s", "e", "w"],
	"use": inventory.allItems,
	"info": inventory.invNames,
	"file": ["save", "load", "quit", "s", "l", "q"]
}

def UpdateInvItems() -> None:
	PossibleArgs["info"] = inventory.invNames

def GetInput() -> list:
	cmd = ""; args = []
	while True:
		inputStr = input("> ")
		cmd = inputStr.split(" ")[0]; args = inputStr.split(" ")[1:]
		if not cmd in cmdList:
			print(errorHandler.ThrowError(errorHandler.ErrorType.UNKNOWNCMD, [cmd]))
			continue
		if len(args) != ExpectedArgs[cmd]:
			print(errorHandler.ThrowError(errorHandler.ErrorType.NUMOFARGS, [cmd, len(args), ExpectedArgs[cmd]]))
			continue
		if cmd == "info": UpdateInvItems()
		try:
			if args[0] not in PossibleArgs[cmd]:
				print(errorHandler.ThrowError(errorHandler.ErrorType.INVALIDARG, [args[0], cmd]))
				continue
		except IndexError: pass

		match cmd:
			case "move":
				match args[0]:
					case ["north", "n"]: return [InputActions.MOVEUP, ""]
					case ["south", "s"]: return [InputActions.MOVEDOWN, ""]
					case ["east", "e"]: return [InputActions.MOVERIGHT, ""]
					case ["west", "w"]: return [InputActions.MOVELEFT, ""]
			case "use": return [InputActions.USEITEM, args[0]]
			case "info": return [InputActions.ITEMINFO, args[0]]
			case "inv": return [InputActions.VIEWINV, ""]
			case "help": return [InputActions.CMDLIST, ""]
			case "?": return [InputActions.HINT, ""]
			case "file":
				match args[0]:
					case ["save", "s"]: return [InputActions.SAVE, ""]
					case ["load", "l"]: return [InputActions.LOAD, ""]
					case ["quit", "q"]: return [InputActions.QUIT, ""]
