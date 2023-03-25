# Functions
def chars_from_str(string: str) -> list:
	chars = []
	chars[:0] = string
	return chars

def generate_2d_list(filler, dimensions: tuple) -> list[list]:
	output = []
	for i in range(dimensions[1]):
		output.append([filler for j in range(dimensions[0])])
	return output

def wait_until(condition: bool, should_reset: bool = False):
	while condition is False: pass
	if should_reset: condition = False