# Built-In Libraries
from enum import Enum
from enum import auto
from json import dumps, loads
# Custom Libraries
from errorHandler import ThrowError, ErrorType
from util import Vector2
import inventory
import narrate

# Classes
class Player:
	'''A player object.'''
	def __init__(self, pos: Vector2) -> None:
		self.pos = pos
	def __str__(self) -> str: return f"Player Object at {self.pos}"
	def ToDict(self) -> dict:
		'''Returns the player as a dictionary.'''
		jsonStr = dumps(self, default=lambda o: o.__dict__, indent="\t")
		return loads(jsonStr)
	@staticmethod
	def FromDict(obj: dict):
		'''Returns an instance of the player from a dictionary.'''
		return Player(Vector2.FromDict(obj["pos"]))

	def PlaceInMap(self) -> None:
		'''Places the player in the room based on their current position.'''
		narrate.map[self.pos.y][self.pos.x] = narrate.TilePresets.Player()
	def Move(self, direction: str) -> None:
		'''Moves the player in the given direction if possible.'''
		match direction:
			case "l": inputVector = Vector2.West()
			case "r": inputVector = Vector2.East()
			case "u": inputVector = Vector2.North()
			case "d": inputVector = Vector2.South()
			case _: raise ValueError(ThrowError(ErrorType.INVALIDARG, [direction, "move"]))
		newPos = Vector2.Add(self.pos, inputVector)
		newTile = narrate.map[newPos.y][newPos.x]
		match newTile["type"]:
			case "wall":
				print("A wall blocks your path.")
				return
			case "passage":
				# room changing crap
				return
			case "item": inventory.IncreaseItemCount(newTile["id"])
		# this code will only run if the new tile was air or an item
		narrate.map[self.pos.y][self.pos.x] = narrate.TilePresets.Air()
		narrate.map[newPos.y][newPos.x] = narrate.TilePresets.Player()
		self.pos = newPos

class InputActions(Enum):
	'''An enumeration of all possible actions the player can take.'''
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

# Constants
MUTABLEACTIONS = (
	InputActions.MOVEUP,
	InputActions.MOVEDOWN,
	InputActions.MOVELEFT,
	InputActions.MOVERIGHT,
	InputActions.USEITEM,
)

CMDLIST = (
	"w",
	"s",
	"a",
	"d",
	"move",
	"use",
	"info",
	"inv",
	"help",
	"?",
	"file"
)

EXPECTEDARGS = {
	"w": 0,
	"s": 0,
	"a": 0,
	"d": 0,
	"move": 1,
	"use": 1,
	"info": 1,
	"inv": 0,
	"help": 0,
	"?": 0,
	"file": 1
}

# Variables
PossibleArgs = {
	"move": ["north", "south", "east", "west", "n", "s", "e", "w"],
	"use": inventory.ITEMPRESETS,
	"info": inventory.invNames,
	"file": ["save", "load", "quit", "s", "l", "q"]
}

# Functions
def UpdateInvItems() -> None:
	'''Updates the possible arguments for the "info" command to match what is inside the inventory.'''
	PossibleArgs["info"] = inventory.invNames

def GetInput() -> list:
	'''Get an input from the player and returns a list with the input action and argument(s).'''
	cmd = ""; args = []
	# loop until the input is valid
	while True:
		# get the raw input
		inputStr = input("> ")
		# split the input into a command and the arguments
		cmd = inputStr.split(" ")[0]; args = inputStr.split(" ")[1:]
		# throw an error if the command isn't valid
		if not cmd in CMDLIST:
			print(ThrowError(ErrorType.UNKNOWNCMD, [cmd]))
			continue
		# throw an error if the number of arguments isn't right
		if len(args) != EXPECTEDARGS[cmd]:
			print(ThrowError(ErrorType.NUMOFARGS, [cmd, len(args), EXPECTEDARGS[cmd]]))
			continue
		# update the possible arguments for the info command if needed
		if cmd == "info": UpdateInvItems()
		# throw an error if the argument is not valid
		try:
			if args[0] not in PossibleArgs[cmd]:
				print(ThrowError(ErrorType.INVALIDARG, [args[0], cmd]))
				continue
		except IndexError: pass

		# return the corresponding stuff
		match cmd:
			case "w": return [InputActions.MOVEUP, ""]
			case "s": return [InputActions.MOVEDOWN, ""]
			case "a": return [InputActions.MOVELEFT, ""]
			case "d": return [InputActions.MOVERIGHT, ""]
			case "move":
				match args[0]:
					case "north" | "n": return [InputActions.MOVEUP, ""]
					case "south" | "s": return [InputActions.MOVEDOWN, ""]
					case "east" | "e": return [InputActions.MOVERIGHT, ""]
					case "west" | "w": return [InputActions.MOVELEFT, ""]
			case "use": return [InputActions.USEITEM, args[0]]
			case "info": return [InputActions.ITEMINFO, args[0]]
			case "inv": return [InputActions.VIEWINV, ""]
			case "help": return [InputActions.CMDLIST, ""]
			case "?": return [InputActions.HINT, ""]
			case "file":
				match args[0]:
					case "save" | "s": return [InputActions.SAVE, ""]
					case "load" | "l": return [InputActions.LOAD, ""]
					case "quit" | "q": return [InputActions.QUIT, ""]