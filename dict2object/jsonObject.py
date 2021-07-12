from typing import Union
from .errorException import (ErrorDataType, numberInKeysNotAllowed)
"""
OPENSOURCE SIAPAPUN BOLEH MENGEDIT INI DENGAN CATATAN MEMASUKAN URL REPO YG ASLI
"""
inden = "\t"
def jsonSerialize(js:Union[list, dict, tuple], level=1) -> str:
    global indent
    indent = inden
    data   = ""
    indent = " "*indent if isinstance(indent, int) else indent
    if isinstance(js, dict):
        data = "{\n"
        for i in js.keys():
            if type(js[i]) in [list, dict, tuple]:
                data+=indent*level+jsonSerialize(js[i], level+1)+",\n"
            elif isinstance(js[i], str):
                data+=indent*level+i.__str__()+f":\"{js[i]}\",\n"
            else:
                data+=indent*level+i.__str__()+f":{js[i]},\n"
        else:
            data = data.strip(",\n")+"\n"+indent*(level-1)+"}"
    elif isinstance(js, list) or isinstance(js, tuple):
        data = "[\n"
        for i in js:
            if type(i) in [list, dict, tuple]:
                data+=indent*level+jsonSerialize(i, level+1)+",\n"
            else:
                data+=indent*level+i.__str__()+",\n"
        else:
            data = data.strip(",\n")+"\n"+indent*(level-1)+"]"          
    return data

class jsObject:
    def __init__(self) -> None:
        pass
    def __repr__(self) -> str:
        nd = {}
        dc=set(dir(self)) - {'__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__'} 
        for i in dc:
            nd.update({i:getattr(self, i)})
        return jsonSerialize(nd)
    def __str__(self) -> str:
        return self.__repr__()


def toObject(js:Union[list, dict, tuple], indent:Union[int, str]="\t") -> Union[jsObject, tuple, list]:
    global inden
    inden = indent
    if not type(js) in [dict, list, tuple]:
        raise ErrorDataType()
    try:
        if type(js) in [list, tuple]:
            data = []
            for i in js:
                if type(i) in [list, dict, tuple]:
                    data.append(toObject(i, indent))
                else:
                    data.append(i)
            return type(js)(data)
        elif isinstance(js, dict):
            obj = jsObject()
            for i in js.keys():
                if type(js[i]) in [list, dict, tuple]:
                    setattr(obj,i.replace(" ","_"),toObject(js[i], indent))
                else:
                    setattr(obj, i.replace(" ","_"), js[i])
            return obj
        else:
            return js
    except AttributeError:
        raise numberInKeysNotAllowed()
