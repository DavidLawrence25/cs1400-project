# Library Imports
import narrate
import util
# Game Loop
room = narrate.LoadMapFromFile(util.Vector2(0, 0))
print(narrate.GetMapString(room))