import base64 as ba
import rcssmin as rc

def load_str(file_path):
    '''
    Reads a text-based file (file_path) and returns a string that
    contains the entire contents of the file. If file_path is relative,
    it must be relative to the current working directory.
    '''
    with open(file_path) as file:
        return file.read()

def load_css(file_path):
    '''
    Reads a CSS file (file_path) and returns a minified CSS string. If
    file_path is relative, it must be relative to the current working
    directory.
    '''
    return rc.cssmin(load_str(file_path))

def load_base64(file_path):
    '''
    Reads a text-based file (file_path) and returns a base64-encoded
    string that contains the entire contents of the file. If file_path
    is relative, it must be relative to the current working directory.
    '''
    return ba.b64encode(load_str(file_path).encode()).decode()
