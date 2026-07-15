import os
import math
from functools import wraps
from exceptions import CriticalFileAccessError


def safe_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        target_path = kwargs.get('path') or (args[1] if len(args) > 1 else None)

        if target_path is not None and os.path.exists(target_path):

            read_permission = os.access(target_path, os.R_OK)
            write_permission = os.access(target_path, os.W_OK)

            if not read_permission or not write_permission:
                raise CriticalFileAccessError(f"Security Error: Required privileges missing for '{target_path}'.")
        else:
            if target_path == "":
                raise CriticalFileAccessError("Security Error: Target absolute path cannot be empty.")

        return func(*args, **kwargs)

    return wrapper


def format_size_logarithmic(size_in_bytes):
    if size_in_bytes == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)

    return f"{s} {units[i]}"