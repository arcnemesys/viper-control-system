import os
import configparser
from utils import repository_path, repository_file
# 
class Repository(object):
    """A git repository"""
    work_tree = None
    git_dir = None
    git_config = None

    def __init__(self, path, git_force=False):
        self.work_tree = path
        self.git_dir = os.path.join(path, ".git")

        if not (git_force or os.path.isdir(self.git_dir)):
            raise Exception("%s is not a Git repository.")
        
        self.config_parser = configparser.ConfigParser()
        config = repository_file(self, "config")

        if config and os.path.exists(config):
            self.git_config.read([config])
        elif not git_force:
            raise Exception("Git configuration file is missing.")
        
        if not git_force:
            version = int(self.git_config.get("core", "repositoryformatversion"))
            if version != 0:
                raise Exception("repository format version %s is not supported" % version)

