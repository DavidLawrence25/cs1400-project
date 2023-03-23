class Event(object):
	def __init__(self) -> None:
		self.__event_handlers = []

	def __iadd__(self, handler):
		self.__event_handlers.append(handler)
		return self

	def __isub__(self, handler):
		self.__event_handlers.remove(handler)
		return self

	def __call__(self, *args, **kwargs) -> None:
		for handler in self.__event_handlers: handler(*args, **kwargs)

	def add_subscribers(self, *args) -> None:
		for handler in args: self += handler

	def remove_subscribers(self, *args) -> None:
		for handler in args: self -= handler