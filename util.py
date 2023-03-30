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

class Vector2Int:
	def __init__(self, x: int, y: int) -> None:
		self.__x = x
		self.__y = y

	@property
	def x(self) -> int: return self.__x

	@x.setter
	def x(self, new_x: int | float) -> None:
		if type(new_x) in (int, float): self.__x = int(new_x)
		else: pass #! ERROR

	@property
	def y(self) -> int: return self.__y

	@y.setter
	def y(self, new_y: int | float) -> None:
		if type(new_y) in (int, float): self.__y = int(new_y)
		else: pass #! ERROR

	def __eq__(self, vector) -> bool:
		return self.__x == vector.x and self.__y == vector.y

	def __add__(self, vector):
		return Vector2Int(self.__x + vector.x, self.__y + vector.y)

	def __sub__(self, vector):
		return Vector2Int(self.__x - vector.x, self.__y - vector.y)

	def __iadd__(self, vector):
		self = self + vector
		return self

	def __isub__(self, vector):
		self = self - vector
		return self

	@staticmethod
	def zero(): return Vector2Int(0, 0)

	@staticmethod
	def up(): return Vector2Int(0, 1)

	@staticmethod
	def down(): return Vector2Int(0, -1)

	@staticmethod
	def left(): return Vector2Int(-1, 0)

	@staticmethod
	def right(): return Vector2Int(1, 0)