from math import sqrt, atan, cos, pi, tau

def PosMult(x: int | float) -> int: return 1 if x > 0 else 0
def NegMult(x: int | float) -> int: return 1 if x < 0 else 0

def RadToDeg(a: int | float) -> float: return a * 180 / pi
def DegToRad(a: int | float) -> float: return a * pi / 180

def CharsFromStr(string: str) -> list:
	ls = []
	ls[:0] = string
	return ls

class Vector2:
	def __init__(self, x: int | float, y: int | float) -> None:
		self.x = x
		self.y = y
	def __str__(self) -> str: return f"Vector2({self.x}, {self.y})"

	def Length(self) -> float: return sqrt(self.x ** 2 + self.y ** 2)
	def Angle(self, isRad = True) -> float:
		radAngle = pi * NegMult(self.x) + tau * NegMult(self.y) * PosMult(self.x) + atan(self.y / self.x)
		if isRad: return radAngle
		else: return RadToDeg(radAngle)
	def ToIndex(self, w) -> int: return self.y * (w + 1) + self.x

	@staticmethod
	def Add(a, b): return Vector2(a.x + b.x, a.y + b.y)
	@staticmethod
	def Subtract(a, b): return Vector2(a.x - b.x, a.y - b.y)
	@staticmethod
	def Scale(a, scalar): return Vector2(a.x * scalar, a.y * scalar)
	@staticmethod
	def AngleBetween(a, b, isRad = True) -> float:
		raw = abs(a.Angle(isRad) - b.Angle(isRad))
		if isRad: return min(raw, tau - raw)
		else: return min(raw, 360 - raw)
	@staticmethod
	def DotProd(a, b) -> int | float: return a.Length() * b.Length() * cos(Vector2.AngleBetween(a, b))