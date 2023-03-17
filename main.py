# Library Imports
import narrate
import inputHandler
import inventory
import util
import json

# Variable Declarations
vars = {}
lastAction = None

# Functions
def SaveGame() -> None:
	narrate.SaveMapToFile(vars["currentRoom"])
	inventory.SaveInv()
	# save variables
	jsonVars = {k: v.ToDict() for k, v in vars.items()}
	jsonStr = json.dumps(jsonVars, indent="\t")
	with open(r"SaveFile\variables.json", "w") as file: file.write(jsonStr)
	# more save functions?

def LoadGame() -> None:
	# load variables
	with open(r"SaveFile\variables.json", "r") as file: data = json.load(file)
	vars["player"] = inputHandler.Player.FromDict(data["player"])
	vars["currentRoom"] = util.Vector2.FromDict(data["currentRoom"])
	# map and inventory
	narrate.LoadMapFromFile(vars["currentRoom"])
	inventory.LoadInv()
	# more load functions?

# Game Loop
LoadGame() # !IMPORTANT: This will be called from the title screen.
while True:
	print(narrate.GetMapString(narrate.map))
	inputAction, arg = inputHandler.GetInput()
	match inputAction:
		case inputHandler.InputActions.MOVELEFT: vars["player"].Move("l")
		case inputHandler.InputActions.MOVERIGHT: vars["player"].Move("r")
		case inputHandler.InputActions.MOVEUP: vars["player"].Move("u")
		case inputHandler.InputActions.MOVEDOWN: vars["player"].Move("d")
		case inputHandler.InputActions.USEITEM: inventory.UseItem(arg)
		case inputHandler.InputActions.ITEMINFO: pass # make a function to print the item info from a specific address in narration.txt
		case inputHandler.InputActions.VIEWINV: print(inventory.GetInvString())
		case inputHandler.InputActions.HINT: pass # make a function to print the hint based on the progress and/or room
		case inputHandler.InputActions.CMDLIST: print(narrate.GetString(1))
		case inputHandler.InputActions.SAVE: SaveGame()
		case inputHandler.InputActions.LOAD: LoadGame()
		case inputHandler.InputActions.QUIT:
			if lastAction in inputHandler.MUTABLEACTIONS:
				response = input("You have unsaved progress. Would you like to save first? > ")
				match response:
					case "yes" | "y": SaveGame()
					case "no" | "n": break
					case "cancel" | "c": continue
			else: break
	lastAction = inputAction