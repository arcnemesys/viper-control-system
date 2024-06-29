from os.path import join, exists, isdir
from os import makedirs, listdir
from repository import Repository
from configparser import ConfigParser
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

def create_repository(path):
    """Creates a repository at a specified path."""

    repository = Repository(path, True)
    
    work_tree = repository.work_tree
    git_dir = repository.git_dir

    if exists(work_tree):
        if not isdir(work_tree):
            raise Exception("%s is not a directory." % path)
        if exists(git_dir) and listdir(git_dir):
            raise Exception("The directory %s is not empty." % path)
    else:
        makedirs(work_tree)
    
    assert repository_directory(repository, "branches", mkdir=True)
    assert repository_directory(repository, "objects", mkdir=True)
    assert repository_directory(repository, "refs", "tags", mkdir=True)
    assert repository_directory(repository, "refs", "heads", mkdir=True)

    with open(repository_file(repository, "description"),"w") as repository_file:
        repository_file.write("Repository is un-named. Edit this file to name it.")
    
    with open(repository_file(repository, "HEAD"), "w") as repository_file:
        repository_file.write("ref: refs/heads/master\n")
    
    with open(repository_file(repository, "config"), "w") as repository_file:
        git_config = default_config()
        git_config.write(repository_file)

    return repository

def default_config():
    config = ConfigParser()

    config.add_section("core")
    config.set("core", "repositoryformatversion", "0")
    config.set("core", "filemode", "false")
    config.set("core", "bare", "false")
