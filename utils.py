from os.path import join, exists, isdir
from os import makedirs
from collections import OrderedDict
def repository_path(repository, *path):
    """Generate path for the repository git directory."""
    return join(repository.git_dir, *path)

def repository_file(repository, *path, mkdir=False):
    """Generates a path to a repository, creating the contents of *path if not existing."""

    if repository_directory(repository, *path[:-1], mkdir=mkdir):
        return repository_path(repository, *path)

def repository_directory(repository, *path, mkdir=False):
    """Generates a path to directory, creating the contents of *path if not existing and `mkdir` is true."""

    path = repository_path(repository, *path)

    if exists(path):
        if isdir(path):
            return path
        else:
            raise Exception("%s is not a directory." % path)
    
    if mkdir:
        makedirs(path)
        return path
    else:
        return None

def parse_commit(raw, start=0, kv_map=None):
    if not kv_map:
        kv_map = OrderedDict()
    
    space = raw.find(b' ', start)
    newline = raw.find(b'\n', start)

    if (space < 0) or (newline < space):
        assert newline == start

        kv_map[None] = raw[start+1:]
        return kv_map
    
    key = raw[start:space]

    end = start

    while True:
        end = raw.find(b'\n', end+1)

        if raw[end+1] != ord(' '): break

    value = raw[space+1:end].replace(b'\n', b'\n')

    if key in kv_map:
        if type(kv_map[key]) == list:
            kv_map[key].append(value)
        else:
            kv_map[key] = [ kv_map[key], value]
    else:
        kv_map[key] = value
    
    return parse_commit(raw, start=end+1, kv_map=kv_map)