class Event(object):
	instances = []

	def __init__(self, name: str) -> None:
		self.NAME = name
		self.__event_handlers = []
		self.instances.append(self)

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

class Listener(object):
	@staticmethod
	def get_event(name: str):
		matches = [inst for inst in Event.instances if inst.name == name]
		return matches[0]

	def subscribe(self, event_name: str, func) -> None:
		event = Listener.get_event(event_name)
		event += func

	def unsubscribe(self, event_name: str, func) -> None:
		event = Listener.get_event(event_name)
		event -= func
