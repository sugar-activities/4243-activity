
import os

def get_dir():
    path = os.path.dirname(__file__)
    if path == '':
        path = os.path.abspath('.')
    return os.path.join(path, 'images/')

