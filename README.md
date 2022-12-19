## Install
```bash
$ pip install git+https://github.com/krypton-byte/dict2object
```
### Convert Dict Datatype to Javascript Object Like
```python
>>> from dict2object import JSObject
>>> js=JSObject(indent=' '*4).fromDict({
        'a':3,
        '1':10,
        'add':(lambda a, b: a.__add__(b))
})
>>> js
{
    add: <function <lambda> at 0x7f9b5f4bd1b0>,
    '1': 10,
    a: 3
}

>>> js.add(9, 11)
20
>>> js.add(js['1'], js.a)
13
```
