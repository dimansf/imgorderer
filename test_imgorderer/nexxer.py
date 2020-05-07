import unittest

from ..nextgen.nexxer import Program

def program_factory():
    return Program()

class ProgramTest(unittest.TestCase): 
    def setUp(self):
        super().setUp()
        print('this is setup')
    def test_calc_hash(self):

        pass
    def test_full_compare(self):
        pass
    def test_drain_files(self):
        pass
    def test_complex_comparision(self):
        pass
    def test_soft_move_file(self):
        pass
    def test_accumulate_files(self):
        pass
    def test_is_correct_file(self):
        pass
    def test_put_in_hashtable(self):
        pass


if __name__ == '__main__':
    unittest.main()