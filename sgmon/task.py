import shelve
import threading


class TaskManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if getattr(cls, '_instance') is None:
            cls._instance = super(TaskManager, cls).__new__(
                cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._lock = threading.Lock()
        self._db_path = "./tasks.db"
        with shelve.open(self._db_path, writeback=True) as db:
            if 'tasks' not in db:
                db['tasks'] = []

    def add_task(self, task):
        with self._lock:
            with shelve.open(self._db_path, writeback=True) as db:
                if task not in db['tasks']:
                    db['tasks'].append(task)

    def remove_task(self, task):
        with self._lock:
            with shelve.open(self._db_path, writeback=True) as db:
                if task in db['tasks']:
                    db['tasks'].remove(task)

    def get_tasks(self):
        with shelve.open(self._db_path, flag='r') as db:
            all_tasks = db['tasks']

        return all_tasks
