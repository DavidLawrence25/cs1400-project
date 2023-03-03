from enum import Enum
from enum import auto
import errorHandler
import inventory

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
	"?",
	"file"
]

ExpectedArgs = {
	"move": 1,
	"use": 1,
	"info": 1,
	"inv": 0,
	"?": 0,
	"file": 1
}

PossibleArgs = {
	"move": ["north", "south", "east", "west", "n", "s", "e", "w"],
	"use": inventory.allItems,
	"info": inventory.GetInvItemNames(),
	"file": ["save", "load", "quit", "s", "l", "q"]
}

def GetInput() -> list[InputActions, str]:
	cmd = ""; args = []
	while True:
		inputStr = input("Enter a Command: ")
		cmd = inputStr.split(" ")[0]; args = inputStr.split[1:]
		if not cmd in cmdList:
			print(errorHandler.throwError(errorHandler.ErrorType.UNKNOWNCMD, [cmd]))
			continue
		if len(args) == ExpectedArgs[cmd]:
			print(errorHandler.throwError(errorHandler.ErrorType.NUMOFARGS, [cmd, len(args), ExpectedArgs[cmd]]))
			continue
		if args[0] in PossibleArgs[cmd]:
			print(errorHandler.throwError(errorHandler.ErrorType.INVALIDARG, [args[0], cmd]))
			continue
		
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
			case "?": return [InputActions.HINT, ""]
			case "file":
				match args[0]:
					case ["save", "s"]: return [InputActions.SAVE, ""]
					case ["load", "l"]: return [InputActions.LOAD, ""]
					case ["quit", "q"]: return [InputActions.QUIT, ""]
