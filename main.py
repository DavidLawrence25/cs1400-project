# Library Imports
import narrate
import inputHandler
import inventory
import util
# Variable/Object Declarations
player = inputHandler.Player(util.Vector2(0, 0)) # note: the position may change based on the starting map
currentRoom = util.Vector2(0, 0)
# Game Loop
while True:
	inputAction, arg = inputHandler.GetInput()
	match inputAction:
		case inputHandler.InputActions.MOVELEFT: player.Move("l")
		case inputHandler.InputActions.MOVERIGHT: player.Move("r")
		case inputHandler.InputActions.MOVEUP: player.Move("u")
		case inputHandler.InputActions.MOVEDOWN: player.Move("d")
		case inputHandler.InputActions.USEITEM: inventory.UseItem(arg)
		case inputHandler.InputActions.ITEMINFO: pass # make a function to print the item info from a specific address in narration.txt
		case inputHandler.InputActions.VIEWINV: pass # make a function to print the current inventory
		case inputHandler.InputActions.HINT: pass # make a function to print the hint based on the progress and/or room
		case inputHandler.InputActions.CMDLIST: print(narrate.GetString(1))
		case inputHandler.InputActions.SAVE:
			narrate.SaveMapToFile(narrate.map, currentRoom)
			# more save functions
		case inputHandler.InputActions.LOAD:
			narrate.LoadMapFromFile(currentRoom)
		case inputHandler.InputActions.QUIT: break