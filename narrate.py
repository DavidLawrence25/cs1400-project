def getString(addr: int) -> str:
    # open the file
    file = open("narration.txt", "r")
    # make address strings to check against
    addrStart = f"%{addr}%\n"
    addrEnd = f"%{addr + 1}%\n"
    # get the text
    text = ""
    isReading = False
    for line in file:
        if isReading:
            if line == addrEnd: break
            else: text += line
        if line == addrStart: isReading = True
    file.close()
    return text.strip()