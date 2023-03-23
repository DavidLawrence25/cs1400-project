class Item:
	def __init__(self,
				id: str = "unknown_item",
				name: str = "Unknown Item",
				count: int = 1,
				expendable: bool = True,
				func: str = "") -> None:
		self.__id = id
		self.__name = name
		self.__count = count
		self.__expendable = expendable
		self.__func = func

	def __str__(self) -> str:
		return f"Item '{self.__name}' ({self.__count})"

	@property
	def id(self) -> str: return self.__id

	@id.setter
	def id(self, new_id) -> None:
		if type(new_id) is str and new_id in ALL_IDS: self.__id = new_id
		else: pass # ! ERROR

	@property
	def name(self) -> str: return self.__name

	@name.setter
	def name(self, new_name) -> None:
		if type(new_name) is str: self.__name = new_name
		else: pass # ! ERROR

	@property
	def count(self) -> int: return self.__count

	@count.setter
	def count(self, new_count) -> None:
		try:
			if type(new_count) is int and new_count > 0:
				self.__count = new_count
		except: pass # ! ERROR

	@property
	def expendable(self) -> bool: return self.__expendable

	@expendable.setter
	def expendable(self, new_exp) -> None:
		if type(new_exp) is bool: self.__expendable = new_exp
		else: pass # ! ERROR

	@property
	def func(self) -> str: return self.__func

	@func.setter
	def func(self, new_func) -> None:
		if type(new_func) is str: self.__func = new_func
		else: pass # ! ERROR

	def increment_count(self, increment: int = 1) -> None:
		try: self.__count += increment
		except: pass # ! ERROR
		if self.__count < 1: pass # some sort of inventory function

PRESETS = [
	Item("notepad", "Notepad", 1, False, "open_notepad"),
	Item("sword", "Sword", 16, True, "slash_sword")
]

ALL_IDS = [item.name for item in PRESETS]