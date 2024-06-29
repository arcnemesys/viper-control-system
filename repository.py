from os.path import join, isdir, exists, realpath
from os import listdir, makedirs
from configparser import ConfigParser
from utils import repository_file, repository_directory
# 
class Repository(object):
    """A git repository"""
    work_tree = None
    git_dir = None
    git_config = None

    def __init__(self, path, git_force=False):
        self.work_tree = path
        self.git_dir = join(path, ".git")

        if not (git_force or isdir(self.git_dir)):
            raise Exception("%s is not a Git repository.")
        
        self.config_parser = ConfigParser()
        config = repository_file(self, "config")

        if config and exists(config):
            self.git_config.read([config])
        elif not git_force:
            raise Exception("Git configuration file is missing.")
        
        if not git_force:
            version = int(self.git_config.get("core", "repositoryformatversion"))
            if version != 0:
                raise Exception("repository format version %s is not supported" % version)

def create_repository(path):
    """Creates a repository at a specified path."""

    global repository 
    
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

        
    with open(repository_file(repository, "description"),"w") as repo_file:
        repo_file.write("Repository is un-named. Edit this file to name it.\n")
    
    with open(repository_file(repository, "HEAD"), "w") as repo_file:
        repo_file.write("ref: refs/heads/master\n")
    
    with open(repository_file(repository, "config"), "w") as repo_file:
        git_config = default_config()
        git_config.write(repo_file)

    return repository

def repository_find(path=".", required=True):

    path = realpath(path)

    if isdir(join(path, ".git")):
        return Repository(path)
    
    parent = realpath(join(path, "."))

    if parent == path:
        if required:
            raise Exception("Unable to find git directory.")
    else:
        return None
    return repository_find(parent, required)

def default_config():
    config = ConfigParser()

    config.add_section("core")
    config.set("core", "repositoryformatversion", "0")
    config.set("core", "filemode", "false")
    config.set("core", "bare", "false")

    return config