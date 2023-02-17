from enum import Enum
from enum import auto
import errorHandler
import inventory

class InputActions(Enum):
    MOVEUP = auto(),
    MOVEDOWN = auto(),
    MOVELEFT = auto(),
    MOVERIGHT = auto(),
    USEITEM = auto(),
    ITEMINFO = auto(),
    VIEWINV = auto(),
    HINT = auto(),
    CMDLIST = auto(),
    SAVE = auto(),
    LOAD = auto(),
    QUIT = auto()

cmdList = [
    "move",
    "use",
    "info",
    "inv",
    "?",
    "file"
]

ExpectedArgs = {
    "move": 1,
    "use": 1,
    "info": 1,
    "inv": 0,
    "?": 0,
    "file": 1
}

PossibleArgs = {
    "move": ["north", "south", "east", "west", "n", "s", "e", "w"],
    "use": inventory.allItems,
    "info": inventory.GetInvItemNames(),
    "file": ["save", "load", "quit", "s", "l", "q"]
}

def GetInput() -> InputActions:
    cmd = ""; args = []
    while True:
        inputStr = input("Enter a Command: ")
        cmd = inputStr.split(" ")[0]; args = inputStr.split[1:]
        if not cmd in cmdList:
            print(errorHandler.throwError(errorHandler.UNKNOWNCMD, [cmd]))
            continue
        
        

