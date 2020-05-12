import unittest
import os
from ..main import Program
from pathlib import Path
from shutil import copy, rmtree




class TestProgram(unittest.TestCase):
    program:Program = None
    abs_path:str = os.path.dirname(os.path.abspath(__file__))
    src:Path = Path(abs_path).joinpath('src')
    dst:Path = Path(abs_path).joinpath('dst')

        # print (f'src is {self.src} \ndst is {self.dst}')
    
    def setUp(self):
        for f in Path(self.src).joinpath('1').iterdir():
            copy(str(f), self.src)
        self.program = Program(self.src, self.dst)
        
    def tearDown(self):
        try:
            rmtree(self.dst)
            [f.unlink() for f in self.src.iterdir() if f.is_file()]
        except:
            print('')
        

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

    def test_sub_drain_files(self):
        self.program.accumulate_files(self.src)
        self.program.sub_drain_files(self.program.hashes['txt'],
        self.dst, self.dst.joinpath('dup'))
        fls = self.file_list(path=self.dst)

        self.assertEqual(len(fls), 2)

    def test_complex_comparision(self):
        fls = self.file_list()
        grps = self.program.complex_comparision(fls)
        self.assertEqual(len(grps), 3)
        self.assertEqual(len(grps[0]), 2)
    
    def test_move_groups(self):
        fls = self.file_list(True)
        d_a = 'dup'
        dup:Path = self.dst.joinpath(d_a)
        self.program.move_groups(fls, self.dst, dup)
        dstf = self.file_list(path=self.dst)
        self.assertEqual(len(dstf), 1)
        dstf = self.file_list(path=dup)

        self.assertEqual(len(dstf), 4)


    def test_soft_move_file(self):
        
        fl = self.file_list().pop()
        self.program.soft_move_file(fl, fl.stem, self.dst)
        self.program.soft_move_file(fl, fl.stem, self.dst)
        
        self.assertEqual(len(self.file_list(path=self.dst)), 2)
        
    def test_notifyAbout(self):
        self.assertTrue(True)

    def test_move(self):
        self.assertTrue(True)
    
    def test_accumulate_files(self):
        self.program.accumulate_files(self.src)
        self.assertEqual(len(self.program.hashes), 2)
        self.assertTrue(len(self.program.hashes['txt']) == 2)
    
    
    def test_put_in_hashtable(self):
        fls = self.file_list()
        for f in fls: self.program.put_in_hashtable(f)
        
        self.assertFalse(self.program.hashes.get('txt') is None)
        self.assertEqual(len(self.program.hashes['txt']), 2 )

    def file_list(self, str_type:bool=False, path:Path=None):
        if path is None: path = self.src
        if not str_type:
            return [x for x in path.iterdir() if x.is_file()]
        else:
            return [str(x) for x in path.iterdir() if x.is_file()]

    


if __name__ == '__main__':
    unittest.main()


