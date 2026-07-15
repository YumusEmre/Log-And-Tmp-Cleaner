# exceptions.py

class CriticalFileAccessError(Exception):
    def __init__(self, message="Access denied or file locked."):
        self.message = message
        super().__init__(self.message)