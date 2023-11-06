from src.utils import setup_dbqa
from db_build import run_db_build
class DatabaseManager:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._connection = None
            cls._instance._is_local = None
            cls._instance._context = None
        return cls._instance

    def get_context(self):
        return self._context
    
    def switch_context(self,path):
        self._context = path

    def connect(self):
        self._connection = setup_dbqa(self._is_local,path=self._context)
        return self._connection
    
    def set_local_true(self):
        self._is_local = True
    
    def set_local_false(self):
        self._is_local = False

    def process_new_items(self,path,vec_path):
        run_db_build(self._is_local,path=path, vec_path=vec_path)
        return None
