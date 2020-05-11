import unittest
import os
from ..main import Program
from pathlib import Path
from shutil import copy, rmtree




class TestProgram(unittest.TestCase):
    program:Program = None
    abs_path:str = os.path.dirname(os.path.abspath(__file__))
    src:str = Path(abs_path).joinpath('src')
    dst:str = Path(abs_path).joinpath('dst')

        # print (f'src is {self.src} \ndst is {self.dst}')
    
    def setUp(self):
        for f in Path(self.src).joinpath('1').iterdir():
            copy(str(f), self.src)
        self.program = Program(self.src, self.dst)
        
    def tearDown(self):
        try:
            rmtree(self.dst)
        except:
            print(f'{self.dst} is not exist')
        

    def test_calc_hash(self):
        self.assertTrue(True)
        
    def test_main(self):
        pass
    def test_full_compare(self):
        a = os.path.join(self.src, 'aaa.txt')
        b = os.path.join(self.src, 'aaa copy.txt')
        c = os.path.join(self.src, 'abc copy.txt')
        self.assertTrue(self.program.full_compare(a, b))
        self.assertFalse(self.program.full_compare(a, c))

    def test_drain_files(self):
        self.assertTrue(True)
        
    def test_complex_comparision(self):
        fls = self.file_list(self.src, False)
        res = self.program.complex_comparision(fls)
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 2)
    
    def test_soft_move_file(self):
        fls = self.file_list(self.src, False)
        self.program.soft_move_file(fls, self.dst)
        fls = [x for x in Path(self.dst).iterdir()]
        self.assertEqual(len(fls), 4)
        
    def test_move(self):
        self.assertTrue(True)
    def test_accumulate_files(self):
        self.program.accumulate_files(self.src)
        self.assertEqual(len(self.program.hashes), 2)
    def test_is_correct_file(self):
        self.assertTrue(True)
    def test_put_in_hashtable(self):
        p = self.file_list(self.src).pop()
        self.program.put_in_hashtable(p)
        hs = self.program.calc_hash(p)
        self.assertTrue(self.program.hashes.get(hs, -12) != -12)

    def file_list(self, p:str, orig_e:bool=True):
        if orig_e:
            return [x for x in Path(self.src).iterdir() if x.is_file()]
        else:
            return [str(x) for x in Path(self.src).iterdir() if x.is_file()]

    def test_put_in_hashtable(self):
        pass


if __name__ == '__main__':
    unittest.main()


