from datetime import datetime
class Logger:
    levels = ('debug', 'warning', 'info')

    def __init__(self, file='./log.txt', default_log_level=0, namespace:str='default namespace'):
        super().__init__()
        self.file = file
        self.namespace = namespace
        self.default_log_level = default_log_level % 3
    
    def namespace(self, namespace:str):
        return Logger(self.file, self.default_log_level, namespace)

    def log(self, message='', log_level=None, ccls=None):
        if not log_level: log_level = self.default_log_level
        now = datetime.now()
        tt = f'{now.day}\{now.month}\{now.year} {now.second}:{now.minute}:{now.hour}'
        prefix = ccls if ccls is not None else self.namespace
        with open(self.file, 'a+') as f:
            f.write(f'{tt} - LogLevel({self.levels[self.default_log_level].capitalize()}) - {message} in {prefix}')
        