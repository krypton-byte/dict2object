## Install
```bash
$ pip install dictionary-to-object
```
## <u> Merubah data dari dictionary ke object</u>
```python
>>> from json_object import toObject
>>> js = toObject({'a':'b',"x":"e",'z':(lambda x:x+1)}, indent=4)
>>> js
{
        a:"b",
        x:"e",
        z:<function <lambda> at 0x7f71f83a0310>
}
>>> js.z(20)
21
```