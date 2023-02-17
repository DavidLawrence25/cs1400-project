import json
import errorHandler

class Item:
    def __init__(self, name: str, count: int, expendable: bool, function: str):
        if type(name) is str: self.name = name
        else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{name=}".split("=")[0], type(name), str]))
        if type(count) is int: self.count = count
        else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{count=}".split("=")[0], type(count), int]))
        if type(expendable) is bool: self.expendable = expendable
        else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{expendable=}".split("=")[0], type(expendable), bool]))
        if type(function) is str: self.function = function
        else: raise TypeError(errorHandler.throwError(errorHandler.ErrorType.INITVARTYPE, [f"{function=}".split("=")[0], type(function), str]))

inv = {
    0: Item("Notepad", 1, False, "openNotepad"),
    1: Item("Sword", 1, True, "slashSword")
}