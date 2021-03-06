from dict2object import JSObject
import unittest

class testModule(unittest.TestCase):
    def test_lambdas(self):
        self.assertEqual(JSObject().fromDict({'x':1, 'y':[1,2,3,{'z':(lambda x:x*2)}]}).y[3].z(5), 10, "Should be 10")
    def test_dict(self):
        self.assertEqual(JSObject().fromDict({'a':[1,2,3,[{'a':1,'b':2}]]}).a[3][0].a, 1, "Should be 1")
    def test_array_and_string(self):
        self.assertEqual(JSObject().fromDict([0,1,2,3,4,[1,2,3,4,{'a':{'x':"s"}}]])[5][4].a.x, "s", "Should be s")
    def test_object(self):
        self.assertEqual(JSObject().fromDict({"toObject":JSObject}).toObject().fromDict({"x":"z"}).x, "z", "Should be z")
    def test_complex(self):
        self.assertEqual(JSObject().fromDict({"hello":complex(15)}).hello, complex(15), f"Should be {complex(15)}")
    def test_import(self):
        self.assertEqual(JSObject().fromDict([0,1,2,{'impor':__import__}])[3].impor('dict2object').JSObject().fromDict({"k":[123,{"p":90}]}).k[1].p, 90, "Should be 90")
    def test_dictBehaviour(self):
        self.assertEqual(JSObject().fromDict({'1': 2})['1'], 2)
if __name__ == '__main__':
    unittest.main()