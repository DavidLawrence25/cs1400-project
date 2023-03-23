# Built-In Libraries
from math import sqrt, atan, cos, pi, tau
from json import dumps, loads

# Functions
def pos_mult(x: int | float) -> int: return 1 if x > 0 else 0
def neg_mult(x: int | float) -> int: return 1 if x < 0 else 0

def rad_to_deg(a: int | float) -> float: return a * 180 / pi
def deg_to_rad(a: int | float) -> float: return a * pi / 180

def chars_from_str(string: str) -> list:
	chars = []
	chars[:0] = string
	return chars

# Classes
class Vector2:
	'''A vector with an x and y component.'''
	def __init__(self, x: int | float, y: int | float) -> None:
		self.x = x
		self.y = y
	def __str__(self) -> str: return f"Vector2({self.x}, {self.y})"
	def to_dict(self) -> dict:
		'''Returns the player as a dictionary.'''
		jsonStr = dumps(self, default=lambda o: o.__dict__, indent="\t")
		return loads(jsonStr)
	@staticmethod
	def from_dict(obj: dict):
		'''Returns an instance of the player from a dictionary.'''
		return Vector2(obj["x"], obj["y"])

	def length(self) -> float:
		'''Returns the magnitude of the vector.'''
		return sqrt(self.x ** 2 + self.y ** 2)
	def angle(self, is_rad_mode = True) -> float:
		'''Returns the angle starting from the +x axis.'''
		theta = pi * neg_mult(self.x) + tau * neg_mult(self.y) * pos_mult(self.x) + atan(self.y / self.x)
		if is_rad_mode: return theta
		else: return rad_to_deg(theta)
	def to_index(self, arr_width: int) -> int:
		'''Returns the index corresponding to a position on a 2D array.'''
		return self.y * (arr_width + 1) + self.x

	@staticmethod
	def add(a, b): return Vector2(a.x + b.x, a.y + b.y)
	@staticmethod
	def subtract(a, b): return Vector2(a.x - b.x, a.y - b.y)
	@staticmethod
	def scale(a, scalar): return Vector2(a.x * scalar, a.y * scalar)
	@staticmethod
	def angle_between(a, b, is_rad_mode = True) -> float:
		'''Returns the smallest angle between two vectors.'''
		theta_raw = abs(a.angle(is_rad_mode) - b.angle(is_rad_mode))
		if is_rad_mode: return min(theta_raw, tau - theta_raw)
		else: return min(theta_raw, 360 - theta_raw)
	@staticmethod
	def dot_prod(a, b) -> int | float: return a.length() * b.length() * cos(Vector2.angle_between(a, b))

	@staticmethod
	def zero(): return Vector2(0, 0)
	@staticmethod
	def north(): return Vector2(0, -1)
	@staticmethod
	def south(): return Vector2(0, 1)
	@staticmethod
	def west(): return Vector2(-1, 0)
	@staticmethod
	def east(): return Vector2(1, 0)