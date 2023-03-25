# Built-In Libraries
from os import get_terminal_size, system

# Constants
COMMENT_CHAR = "#"

# Variables
feedback = ""

# Functions
def get_string(addr: int) -> str:
	'''Return a string from the narration file.'''
	# open the file
	with open("narration.txt", "r") as file:
		# make address strings to check against
		addr_start = f"%{addr}%\n"
		addr_end = f"%{addr + 1}%\n"
		# get the text
		text = ""
		is_reading = False
		for line in file:
			if is_reading:
				if line == addr_end: break
				elif line[0] == COMMENT_CHAR: continue
				else: text += line
			if line == addr_start: is_reading = True
	return text.strip()

def display(map_str: str, narration: str, feedback: str) -> None:
	map_lines = map_str.splitlines()
	text_lines = feedback.splitlines()
	if feedback != "": text_lines.append("")
	text_lines.append(*narration.splitlines())
	terminal_w = get_terminal_size().columns
	map_w = len(map_lines[0])
	text_w = terminal_w - map_w
	iter_count = len(map_lines) if len(map_lines) > len(text_lines) else len(text_lines)
	output = ""
	for i in range(iter_count):
		if len(map_lines) > i and len(text_lines) > i: output += f"{text_lines[i]:<{text_w}}{map_lines[i]}\n"
		elif len(text_lines) > i: output += f"{text_lines[i]:<{text_w}}\n"
		else: output += f"{map_lines[i]:>{terminal_w}}\n"
	system("cls"); print(output)