from hashlib import md5
from pathlib import Path
from shutil import move, copy, rmtree
import os
from os.path import join  
from typing import Dict, List, Tuple
import sys  
import re
from random import randint



class Program: 
    # images + videios
    
    hashes:Dict[str, Dict[str, List[str]]] = None
    file_counter:int = 0
    base_dir:Path = None
    copy_dir:Path = None 
    excluded_dst:Path = None 
    safe_mode:bool = True

    def __init__(self, base_dir:str, copy_dir:str, safe_mode:bool=True):
        self.safe_mode = safe_mode
        self.hashes = {}
        self.base_dir = Path(base_dir)
        self.copy_dir = Path(copy_dir)
        self.excluded_dst = Path(copy_dir).joinpath('excluded')
        
        

    def calc_hash(self, file_path:Path):
        with file_path.open('rb') as file1:
            hh = md5(file1.read())
            return hh.hexdigest()


    def main(self,  safe_mode:bool=True):
        self.safe_mode = safe_mode

        print('Группируем файлы по хешу')
        self.accumulate_files(self.base_dir)
        print(f'Всего файлов найдено: {self.file_counter}')

        print('Скидываем все недублированные файлы в общую директорию')
        self.drain_files(self.copy_dir)
    
   

    def full_compare(self, file_name, file_name2):
        with open(file_name, 'rb') as f1, open(file_name2, 'rb') as  f2:
            return f1.read() == f2.read()

    def drain_files(self,copy_dir:Path ):
        for el in self.hashes:
            cp_dir = copy_dir.joinpath(str(el))
            dup_dir = cp_dir.joinpath('duplicates')
            
            
            
            self.sub_drain_files(self.hashes[el], cp_dir, dup_dir)

    def sub_drain_files(self, fls:Dict[str, List[str]], cp_dir:Path, dup_dir:Path):
        """
            Обходим и перемещаем\копируем файлы в общую папку """
        for kk in fls:
            for grp in self.complex_comparision(fls[kk]):
                self.move_groups(grp, cp_dir, dup_dir)
            
    

    def complex_comparision(self, files:List[str]) -> List[List[str]]:
        """
            Раскидываем по группам на основании полного
             сравнения коллекции обьектов"""
        if len(files) == 1: return [files]

        grps = [ [files[0]] ]

        for ffs in files[1:]:
            fl = False
            for grp in grps:
                if self.full_compare(grp[0], ffs):
                    grp.append(ffs)
                    fl = True
                    break
            if not fl:
                grps.append([ffs])
        return grps

    def move_groups(self, grp:List[str],  cp_dir:Path, dup_dir:Path):
        f1 = Path(grp.pop())
        stem = self.soft_move_file(f1, f1.stem, cp_dir)
        for el in grp:
            self.soft_move_file(Path(el), stem, dup_dir)


       
    def soft_move_file(self, ff:Path, stem:str, cp_dir:Path)-> str:
        """
            Перемещаем файлы и именуем по первому имени в коллекции
            ** файлы не медиа расширений переносим в другую директорию
            """
        
        if not cp_dir.exists():  cp_dir.mkdir(parents=True)
        c = 1
        fi = cp_dir.joinpath(stem + ff.suffix)
        while fi.exists():
            c += 1
            fi = cp_dir.joinpath(stem + f'___{str(c)}' + ff.suffix)
        
        self.move(ff, fi)
        self.notifyAbout('Файл скопирован\перемещен в :', str(fi))
        return fi.stem
         
                
    def notifyAbout(self, d:str, ms:str):
        print(f'{d} {ms}')

    def move(self, src:Path, dst:Path):
        if self.safe_mode:
            copy(src, dst)
        else:
            move(src, dst)

    def accumulate_files(self, base_dir:Path):
        """
            Рекурсивно обойти файлы и раскидать по хешам"""
        for d in base_dir.iterdir():
            if d.is_dir():
                self.accumulate_files(d)
            if d.is_file():
                self.put_in_hashtable(d)
        

    def put_in_hashtable(self, f:Path):

        hash = self.calc_hash(f)
        sfx = f.suffix[1:] if len(f.suffix) > 1 else 'no_ext'
        if self.hashes.get(sfx) is None: self.hashes[sfx] = {}
            
        if self.hashes[sfx].get(hash) is None: self.hashes[sfx][hash] = []
            
        self.hashes[sfx][hash].append(str(f))
        self.file_counter += 1


    
        
    
  
if __name__ == "__main__":
    nx = Program(sys.argv[1], sys.argv[2])
    nx.main()
        