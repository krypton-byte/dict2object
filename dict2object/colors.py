from colorama import init, Fore
init()
class Color:
    def __init__(self, name: str, curly: str, square: str, string: str, number: str, comma: str, key: str, colon: str,other: str):
        self.name = name
        self.comma = comma
        self.curly = curly
        self.square = square
        self.key = key
        self.colon_ = colon
        self.string = string
        self.number = number
        self.other = other
    def keys(self, s: str):
        return self.key + s + Fore.RESET
    @property
    def colon(self):
        return self.apply(':')
    @property
    def commas(self):
        return self.comma + ','+self.key
    def apply(self, char):
        if char in ['{','}']:
            return self.curly+char+Fore.RESET
        elif char == ':':
            return self.colon_+': '+Fore.RESET
        elif char in ['[',']']:
            return Fore.RESET+self.square+''+('[' if char == '[' else char)+Fore.RESET
        elif isinstance(char, int):
            return self.number.__str__()+char.__str__()
        elif isinstance(char, str) and (char[-1] in ["'", '"']):
            return self.string+char[0]+char[1:-1]+char[-1]
        else:
            return self.other+char.__str__()+Fore.RESET
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class Colors(list):
    def __init__(self):
        super().__init__([Color(*i) for i in [[
            'Default',
            Fore.LIGHTCYAN_EX,
            Fore.LIGHTMAGENTA_EX,
            Fore.LIGHTGREEN_EX,
            Fore.LIGHTYELLOW_EX,
            Fore.LIGHTBLUE_EX,
            Fore.LIGHTRED_EX,
            Fore.LIGHTCYAN_EX,
            Fore.LIGHTRED_EX
        ]]])
    def Empty(self):
        return Color(*(['']*9))
        