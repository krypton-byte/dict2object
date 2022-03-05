from __future__ import annotations
from typing import (
    Union,
    Optional,
    Any
)
from .errorException import (
    ErrorDataType,
    ObjectOrNumberInKeysNotAllowed
)


class JSObject:
    def __init__(self, indent = '\t', ignore_attr=[]):
        self.__indent = indent
        self.__ignore_attr = ['__slotnames__','__getitem__','__repr__','__str__', 'fromDict', '__init__', 'jsonSerialize', *ignore_attr, '_'+self.__class__.__name__ + '__indent'+'', '_'+self.__class__.__name__ + '__ignore_attr']

    def __repr__(self) -> str:
        nd = {}
        dc=set(dir(self)) - {'__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__'} 
        for i in dc:
            nd.update({i:getattr(self, i)})
        y = self.jsonSerialize(nd, 1)
        return y

    def __str__(self) -> str:
        return self.__repr__()

    def __getitem__(self, name):
        return self.__getattribute__(name)

    def jsonSerialize(self, js:Union[list, dict, tuple], level) -> str:
        data   = ""
        if isinstance(js, dict):
            data = "{\n"
            for i in js.keys():
                if i in self.__ignore_attr:
                    continue
                elif type(js[i]) in [dict]:
                    data+=self.__indent*level+self.jsonSerialize(js[i], level+1)+",\n"
                if isinstance(js[i], (list, tuple)):
                    data+=self.__indent*level+f'{i.__repr__() if i.isnumeric() else i}: '+self.jsonSerialize(js[i], level+1)+",\n"
                elif isinstance(js[i], str):
                    data+=self.__indent*level+(i.__repr__() if i.isnumeric() else i)+f":\"{js[i]}\",\n"
                elif isinstance(js[i], self.__class__):
                    data+=self.__indent*level+f'{i.__repr__() if i.isnumeric() else i}: '+ self.jsonSerialize(js[i].__dict__, level+1)+",\n"
                else:
                    data+=self.__indent*level+(i.__repr__() if i.isnumeric() else i)+f": {js[i]},\n"
            else:
                data = data.strip(",\n")+"\n"+(self.__indent*(level-1))+"}"
        elif isinstance(js, (list, tuple)):
            data = "[\n"
            for i in js:
                if isinstance(i, (list, tuple)):
                    data+=self.__indent*level+self.jsonSerialize(i, level+1)+",\n"
                elif isinstance(i, dict):
                    data+=self.__indent*level+self.jsonSerialize(i, level+1)+",\n"
                elif isinstance(i, self.__class__):
                    data+=self.__indent*level+self.jsonSerialize(i.__dict__, level+1)+",\n"
                else:
                    data+=self.__indent*level+i.__repr__()+",\n"
            else:
                data = data.strip(",\n")+"\n"+self.__indent*(level-1)+"]"          
        return data

    def fromDict(self, js:Union[list, dict, tuple], indent:Optional[str] = None) -> Union[Any, tuple, list]:
        if indent:
            self.__indent = indent
        if not type(js) in [dict, list, tuple]:
            raise ErrorDataType()
        try:
            if type(js) in [list, tuple]:
                data = []
                for i in js:
                    if type(i) in [list, dict, tuple]:
                        data.append(self.fromDict(i, indent))
                    else:
                        data.append(i)
                return type(js)(data)
            elif isinstance(js, dict):
                obj = self.__class__(self.__indent, self.__ignore_attr)
                for i in js.keys():
                    if type(js[i]) in [list, dict, tuple]:
                        setattr(obj,i.replace(" ","_"),self.fromDict(js[i], indent))
                    else:
                        setattr(obj, i.replace(" ","_"), js[i])
                return obj
            else:
                return js
        except AttributeError:
            raise ObjectOrNumberInKeysNotAllowed()
