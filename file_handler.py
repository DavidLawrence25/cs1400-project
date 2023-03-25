from pathlib import Path
from json import dump, load
import interface

APP_ROOT = Path(".")
FILE_PATHS = {
	"maps": APP_ROOT / "SaveFile" / "maps.json",
	"inv": APP_ROOT / "SaveFile" / "inv.json",
	"variables": APP_ROOT / "SaveFile" / "variables.json"
}

class SaveFile(interface.Listener):
	def __init__(self, maps, inventory, variables) -> None:
		self.__maps = maps
		self.__inventory = inventory
		self.__variables = variables

		self.on_file_save = interface.Event("on_file_save")
		self.on_file_load = interface.Event("on_file_load")
		self.on_file_read = interface.Event("on_file_read")
		self.on_file_written = interface.Event("on_file_written")

		self.subscribe("on_input_parsed", self.on_file_save)
		self.subscribe("on_input_parsed", self.on_file_load)

	def save_file(self) -> None:
		with open(FILE_PATHS["maps"], "w") as file:
			dump(self.__maps, file, indent = "\t")
		with open(FILE_PATHS["inv"], "w") as file:
			dump(self.__inventory, file, indent = "\t")
		with open(FILE_PATHS["variables"], "w") as file:
			dump(self.__variables, file, indent="\t")
		self.on_file_save()

	def load_file(self) -> None:
		# blah blah blah
		self.on_file_load()

	def read_file(self, file_path: Path, *args) -> None:
		# blah blah blah
		self.on_file_read()

	def write_file(self, file_path: Path, *args) -> None:
		# blah blah blah
		self.on_file_written()