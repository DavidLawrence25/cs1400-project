# Built-In Libraries
import json
# Custom Libraries
import narrate
import input_handler
import inventory
import util

# Variable Declarations
vars = {}
prev_action = None

# Functions
def save_game() -> None:
	narrate.save_map_to_file(vars["currentRoom"])
	inventory.save_inv()
	# save variables
	parsed_vars = {key: val.to_dict() for key, val in vars.items()}
	vars_data = json.dumps(parsed_vars, indent="\t")
	with open(r"SaveFile\variables.json", "w") as file: file.write(vars_data)
	# more save functions?

def load_game() -> None:
	# load variables
	with open(r"SaveFile\variables.json", "r") as file: data = json.load(file)
	vars["player"] = input_handler.Player.from_dict(data["player"])
	vars["currentRoom"] = util.Vector2.from_dict(data["currentRoom"])
	# map and inventory
	narrate.load_map_from_file(vars["currentRoom"])
	inventory.load_inv()
	# more load functions?

# Game Loop
load_game() # !IMPORTANT: This will be called from the title screen.
while True:
	narrate.display(narrate.get_map_string(narrate.map), narrate.get_string(2), narrate.feedback)
	narrate.feedback = ""
	input_action, arg = input_handler.get_input()
	match input_action:
		case input_handler.InputActions.MOVE_LEFT: vars["player"].Move("l")
		case input_handler.InputActions.MOVE_RIGHT: vars["player"].Move("r")
		case input_handler.InputActions.MOVE_UP: vars["player"].Move("u")
		case input_handler.InputActions.MOVE_DOWN: vars["player"].Move("d")
		case input_handler.InputActions.USE_ITEM: inventory.use_item(arg)
		case input_handler.InputActions.ITEM_INFO: pass # make a function to print the item info from a specific address in narration.txt
		case input_handler.InputActions.VIEW_INV: narrate.feedback = inventory.get_inv_string()
		case input_handler.InputActions.HINT: pass # make a function to print the hint based on the progress and/or room
		case input_handler.InputActions.CMD_LIST: narrate.feedback = narrate.get_string(1)
		case input_handler.InputActions.SAVE: save_game()
		case input_handler.InputActions.LOAD: load_game()
		case input_handler.InputActions.QUIT:
			if prev_action in input_handler.MUTABLE_ACTIONS:
				response = input("You have unsaved progress. Would you like to save first? > ")
				match response:
					case "yes" | "y": save_game()
					case "no" | "n": break
					case "cancel" | "c": continue
			else: break
	prev_action = input_action