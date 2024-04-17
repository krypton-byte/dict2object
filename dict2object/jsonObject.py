from __future__ import annotations
from typing import (
    Union,
    Optional,
    Any,
    TypeVar
)
from .colors import Color, Colors
from .errorException import (
    ErrorDataType,
    ObjectOrNumberInKeysNotAllowed
)
Colors_ = Colors()
T = TypeVar('T')


class JSObject:
    def __init__(self, indent = '\t', color: Optional[Color] = Colors_[0]):
        self.__indent = indent
        self.__color = color if isinstance(color, Color) else Colors_.Empty() 
        self.__dict_data: Union[list, dict, tuple] = {}
    def __repr__(self) -> str:
        y = self.jsonSerialize(self.__dict_data, 1)
        return y

    def __str__(self) -> str:
        return self.__repr__()

    def jsonSerialize(self, js:Union[list, dict, tuple], level, address = []) -> str:
        data   = ""
        if isinstance(js, dict):
            data = self.__color.apply("{")+"\n"
            for i in js.keys():
                if type(js[i]) in [dict]:
                    if id(js[i]) in address:
                        data += self.__indent*level+self.__color.keys(i)+self.__color.colon+self.__color.other+"{.....}\n,"
                    else:
                        addr=address.copy()
                        addr.append(id(js[i]))
                        data+=''+self.__indent*level+self.__color.keys(i)+self.__color.colon+self.jsonSerialize(js[i], level+1, address=addr)+self.__color.commas+"\n"
                elif isinstance(js[i], (list, tuple)):
                    data+=self.__indent*level+f'{self.__color.keys(i.__repr__() if i.isnumeric() else i)}'+self.__color.colon+self.jsonSerialize(js[i], level+1, address=address.copy())+self.__color.commas+"\n"
                elif isinstance(js[i], str):
                    rep = js[i].__repr__()
                    data+=self.__indent*level+self.__color.keys(i if i.isnumeric() else i)+self.__color.colon+self.__color.apply(rep)+self.__color.commas+"\n"
                elif isinstance(js[i], self.__class__):
                    data+=self.__indent*level+f'{self.__color.keys(i.__repr__() if i.isnumeric() else i)}'+self.__color.colon+self.jsonSerialize(js[i].__data_dict, level+1, address=address.copy())+self.__color.commas+"\n"
                else:
                    data+=self.__indent*level+self.__color.keys(i.__repr__() if i.isnumeric() else i)+self.__color.colon+f"{self.__color.apply(js[i])}"+self.__color.commas+"\n"
            else:
                data = data.strip(",\n")+"\n"+(self.__indent*(level-1))+self.__color.apply("}")
        elif isinstance(js, (list, tuple)):
            data = ' '+self.__color.apply("[")+' '+"\n"
            for i in js:
                if isinstance(i, (list, tuple)):
                    if id(i) in address:
                        data += self.__indent*level+'[....]'
                    else:
                        addr=address.copy()
                        addr.append(id(i))
                        data+=self.__indent*level+self.jsonSerialize(i, level+1, address=addr)+self.__color.commas+"\n"
                elif isinstance(i, dict):
                    if id(i) in address:
                        data += self.__indent*level+'{....}'
                    else:
                        addr=address.copy()
                        addr.append(id(i))
                        data+=self.__indent*level+self.jsonSerialize(i, level+1, address=addr)+self.__color.commas+"\n"
                elif isinstance(i, self.__class__):
                    if id(i) in address:
                        data += '$$'
                    else:
                        addr=address.copy()
                        addr.append(id(i))
                        data+=self.__indent*level+self.jsonSerialize(i.__dict__, level+1, address=addr)+self.__color.commas+"\n"
                else:
                    data+=self.__indent*level+self.__color.apply(i.__repr__() if isinstance(i, str) else i)+''+self.__color.commas+"\n"
            else:
                data = data.strip(self.__color.commas+"\n")+"\n"+self.__indent*(level-1)+self.__color.apply("]")        
        return data

    def fromDict(self, js:Union[list, dict, tuple], indent:Optional[str] = None) -> T:
        if indent:
            self.__indent = indent
        if not isinstance(js, (dict, list, tuple)):
            raise ErrorDataType()
        try:
            self.__dict_data = js
            return self
        except Exception:
            raise ObjectOrNumberInKeysNotAllowed()
    def __getattr__(self, __name: str) -> Any:
        g = self.__dict_data[__name]
        if isinstance(g, (dict, list, tuple)):
            return self.__class__().fromDict(g)
        return g
    def __getitem__(self, name: str):
        x = self.__dict_data[name]
        if isinstance(x, (list, tuple, dict)):
            return self.__class__().fromDict(x)
        return x
