from src.utils import setup_dbqa
from db_build import run_db_build
class DatabaseManager:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._connection = None
            cls._instance._is_local = None
        return cls._instance

    def connect(self):
        if self._connection is None:
            self._connection = setup_dbqa(self._is_local)
        return self._connection
    
    def set_local_true(self):
        self._is_local = True
    
    def set_local_false(self):
        self._is_local = False

    def process_new_items(self):
        run_db_build(self._is_local)
        print("Built")
        return None
