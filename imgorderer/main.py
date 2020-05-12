from hashlib import md5
from pathlib import Path
from shutil import move, copy, rmtree
import os
from os.path import join  
from typing import Dict, List, Tuple
import sys  
import re




class Program: 
    # images + videios
    files_extentions:Tuple = ('jpeg', 'jpg',  'png', 'gif',  'bmp', 'thumb' ) + ('mp4','3gp', 'mpeg', 'wmv') 
    hashes:Dict[str, List[str]] = None
    excluded_dst:Path = None
    file_counter:int = 0
    base_dir:str = None
    copy_dir:str = None
    logger = None
   
    use_ext:bool = False
    safe_mode:bool = True

    def __init__(self, base_dir:str, copy_dir:str,files_extentions:Tuple[str]=(), logger = None):
        
        self.hashes = {}
        self.base_dir = base_dir
        self.copy_dir = copy_dir
        self.excluded_dst = Path(copy_dir).joinpath('excluded')
        if logger:
            self.logger = logger.namespace(str(self.__class__))
        self.files_extentions = self.files_extentions + files_extentions

    def calc_hash(self, file_path:Path):
        with file_path.open('rb') as file1:
            hh = md5(file1.read())
            return hh.hexdigest()


    def main(self, use_ext:bool=False, safe_mode:bool=True): 
        self.use_ext = use_ext
        self.safe_mode = safe_mode

        print('Группируем файлы по хешу')
        self.accumulate_files(Path(self.base_dir))
        print(f'Всего файлов найдено: {self.file_counter}')

        print('Скидываем все недублированные файлы в общую директорию')
        self.drain_files(self.copy_dir)
    
   

    def full_compare(self, file_name, file_name2):
        with open(file_name, 'rb') as f1, open(file_name2, 'rb') as  f2:
            return f1.read() == f2.read()


    def drain_files(self, copy_dir):
        """
            Обходим и перемещаем\копируем файлы в общую папку """
        
        for kk in self.hashes:
            if len(self.hashes[kk]) == 1:
                self.soft_move_file(self.hashes[kk], copy_dir)
            if len(self.hashes[kk]) > 1:
                for grp in self.complex_comparision(self.hashes[kk]):
                    self.soft_move_file(grp, copy_dir)
            

    def complex_comparision(self, files:List[str]) -> List[List[str]]:
        """
            Раскидываем по группам на основании полного
             сравнения коллекции обьектов"""
        if len(files) < 1: return

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
        
       
    def soft_move_file(self, file_list:List[str], copy_dir:str) -> str:
        """
            Перемещаем файлы и именуем по первому имени в коллекции
            ** файлы не медиа расширений переносим в другую директорию
            """

        f1 = Path(file_list[0])
        base_dst = Path(copy_dir)
        
        cc = 1
        for ff in file_list:
            fp = Path(ff)
            if not self.is_correct_file(fp): 
                dst = self.excluded_dst
            else: 
                dst = base_dst
            if not dst.exists(): dst.mkdir(parents=True)
            p = dst.joinpath(f1.stem + fp.suffix)
            while p.exists():
                cc += 1
                p = dst.joinpath(f1.stem + f'___-{str(cc)}' + fp.suffix)
            self.move(ff, str(p))
        self.notifyAbout('Файл скопирован\перемещен:', str(p))
           
                
    def notifyAbout(self, d:str, ms:str):
        print(f'{d} {ms}')

    def move(self, src:str, dst:str):
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
        
    def is_correct_file(self, path:Path):
        """
            Проверяет является ли файл изображением или видео в нужном формате"""
        if not self.use_ext:
            return True
        
        try:
            self.files_extentions.index(path.suffix[1:])
            return True
        except:
            return False

    def put_in_hashtable(self, path:Path):
        

        hash = self.calc_hash(path)
        if self.hashes.get(hash) is None:
            self.hashes[hash] = []
            self.hashes[hash].append(str(path))
        else:
            self.hashes[hash].append(str(path))
        self.file_counter += 1


    
        
    
  
if __name__ == "__main__":
    nx = Program(sys.argv[1], sys.argv[2])
    nx.main()
        