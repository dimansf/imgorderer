from hashlib import md5
from pathlib import Path
from shutil import move, copy, rmtree
import os
from os.path import join  
import sys  
import re
from .logger import Logger 



class Program: 
    # images + videios
    files_extentions = ('jpeg', 'jpg',  'png', 'gif',  'bmp' ) + ('mp4','3gp', 'mpeg') 

    def __init__(self, base_dir:str, copy_dir:str,files_extentions:Tuple[str]=None, logger:Logger = None):
        """
            """
        self.hashes:Dict[str, List[str]] = {}
        self.base_dir = base_dir
        self.copy_dir = copy_dir
        self.logger = logger.namespace(str(self.__class__))
        self.files_extentions = self.files_extentions + files_extentions if files_extentions else ()

    def calc_hash(self, file_path:Path):
        with file_path.open('rb') as file1:
            hh = md5(file1.read())
            return hh.hexdigest()


    def main(self): 
        print('Группируем файлы по хешу')
        self.accumulate_files(Path(self.base_dir))

        print('Скидываем все недублированные файлы в общую директорию')
        self.drain_files(self.copy_dir)
    
   

    def full_compare(self, file_name, file_name2):
        f1 = open(file_name, 'rb')
        f2 = open(file_name2, 'rb')
        res =  f1.read() == f2.read()
        f1.close
        f2.close
        return res


    def drain_files(self):
        """
            Обходим и перемещаем файлы в общую папку """
        
        for kk in self.hashes:
            if len(self.hashes[kk]) == 1:
                self.soft_move_file(self.hashes[kk], self.copy_dir)
            if len(self.hashes[kk]) > 1:
                for grp in self.complex_comparision(self.hashes[kk]):
                    self.soft_move_file(grp, self.copy_dir)
            

    def complex_comparision(self, files:List[str]) -> List[List[str]]:
        """
            Раскидываем по группам на основании полного
             сравнения коллекции обьектов"""
        if len(files) < 1: return

        grps = [ files[0]]

        for ffs in files:
            fl = False
            for grp in grps:
                if self.full_compare(grp[0], ffs):
                    grp.append(ffs)
                    fl = True
                    break
            if not fl:
                grps.append([ffs])
        return grps
        
       
    def soft_move_file(self, paths:List[str], copy_dir:str):
        """
            Перемещаем коллекцию элементов и нумеруем по порядку
            ! неизвестно поведение при несовпадении расширений
            ! и при нескольких расширениях"""

        f1 = Path(paths[0])
        res = Path(copy_dir)
        if not res.exists(): res.mkdir()
        cc = 1
        for ff in paths:
            if not res.joinpath(f1.name).exists():
                move(ff, copy_dir)
            else:
                cc += 1
                move(ff, str(res.joinpath(f1.stem +  f'_{str(cc)}' + f1.suffix)))


    def accumulate_files(self, base_dir:Path):
        """
            Рекурсивно обойти файлы и раскидать по хешам"""
        for d in base_dir.iterdir():
            if d.is_dir():
                self.accumulate_files(d)
            if d.is_file():
                self.put_in_hashtable(d)
        
    def is_correct_file(self, path:Path):
        """
            Проверяет является ли файл изображением или видео в нужном формате"""
        try:
            self.files_extentions.index(path.suffix[1:])
            return True
        except:
            return False

    def put_in_hashtable(self, path:Path):
        if not is_correct_file(path): return

        hash = self.calc_hash(path)
        if self.hashes.get(hash) is None:
            self.hashes[hash] = []
            self.hashes[hash].append(str(path))
        else:
            self.hashes[hash].append(str(path))


    
        
    
  
if __name__ == "__main__":
    nx = Program(sys.argv[1], sys.argv[2])
    nx.main()
        