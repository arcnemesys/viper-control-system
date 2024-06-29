from os.path import join, exists, isdir
from os import makedirs
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