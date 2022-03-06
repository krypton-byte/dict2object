from __future__ import annotations
from typing import (
    Union,
    Optional,
    Any
)
from .colors import Color, Colors
from .errorException import (
    ErrorDataType,
    ObjectOrNumberInKeysNotAllowed
)
Colors_ = Colors()

class JSObject:
    def __init__(self, indent = '\t', ignore_attr=[], color: Optional[Color] = Colors_[0]):
        self.__indent = indent
        self.__color = color if isinstance(color, Color) else Colors_.Empty() 
        self.__ignore_attr = ['__slotnames__','__getitem__','__repr__','__str__', 'fromDict', '__init__', 'jsonSerialize', *ignore_attr, '_'+self.__class__.__name__ + '__indent'+'', '_'+self.__class__.__name__ + '__ignore_attr', '_'+self.__class__.__name__ + '__color']

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
            data = self.__color.apply("{")+"\n"
            for i in js.keys():
                if i in self.__ignore_attr:
                    continue
                elif type(js[i]) in [dict]:
                    data+=self.__indent*level+self.jsonSerialize(js[i], level+1)+self.__color.commas+"\n"
                elif isinstance(js[i], (list, tuple)):
                    data+=self.__indent*level+f'{self.__color.keys(i.__repr__() if i.isnumeric() else i)}'+self.__color.colon+self.jsonSerialize(js[i], level+1)+self.__color.commas+"\n"
                elif isinstance(js[i], str):
                    rep = js[i].__repr__()
                    data+=self.__indent*level+self.__color.keys(i if i.isnumeric() else i.__repr__())+self.__color.colon+self.__color.apply(rep[0])+rep[1:-1]+self.__color.apply(rep[-1])+self.__color.commas+"\n"
                elif isinstance(js[i], self.__class__):
                    data+=self.__indent*level+f'{self.__color.keys(i.__repr__()) if i.isnumeric() else i}'+self.__color.colon+self.jsonSerialize(js[i].__dict__, level+1)+self.__color.commas+"\n"
                else:
                    data+=self.__indent*level+self.__color.keys(i.__repr__() if i.isnumeric() else i)+self.__color.colon+f"{self.__color.apply(js[i])}"+self.__color.commas+"\n"
            else:
                data = data.strip(",\n")+"\n"+(self.__indent*(level-1))+self.__color.apply("}")
        elif isinstance(js, (list, tuple)):
            data = ' '+self.__color.apply("[")+' '+"\n"
            for i in js:
                if isinstance(i, (list, tuple)):
                    data+=self.__indent*level+self.jsonSerialize(i, level+1)+self.__color.commas+"\n"
                elif isinstance(i, dict):
                    data+=self.__indent*level+self.jsonSerialize(i, level+1)+self.__color.commas+"\n"
                elif isinstance(i, self.__class__):
                    data+=self.__indent*level+self.jsonSerialize(i.__dict__, level+1)+self.__color.commas+"\n"
                else:
                    data+=self.__indent*level+self.__color.apply(i.__repr__() if isinstance(i, str) else i)+''+self.__color.commas+"\n"
            else:
                data = data.strip(self.__color.commas+"\n")+"\n"+self.__indent*(level-1)+self.__color.apply("]")        
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
                obj = self.__class__(self.__indent, self.__ignore_attr, self.__color)
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
