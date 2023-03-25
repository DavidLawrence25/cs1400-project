import interface

# Variable Declarations
vars = {}
prev_action = None

# Game Loop
# * load game
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