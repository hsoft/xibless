import os

def modified_after(first_path, second_path):
    """Returns True if first_path's mtime is higher than second_path's mtime."""
    try:
        first_mtime = os.stat(first_path).st_mtime
    except EnvironmentError:
        return False
    try:
        second_mtime = os.stat(second_path).st_mtime
    except EnvironmentError:
        return True
    return first_mtime > second_mtime
