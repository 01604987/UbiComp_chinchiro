from micropython import const

# all colors are 1/5 bright
#               "red",   "blue",   "green", "yellow",   "purple", "turkoise"
LIGHTS = const(((64,0,0), (0,64,0), (0,0,64), (64,64,0), (64,0,64), (0,64,64)))

class Led:

    def __init__(self) -> None:
        pass
