import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        super().setUp()
        # print('this is setup')
    def tearDown(self):
        super().tearDown()
        # print('this is teardown')
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('foo'.isupper(), 'this is message')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # Проверим, что s.split не работает, если разделитель - не строка
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()