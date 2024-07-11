from repository import create_repository, repository_find
from git_object import read_object, find_object
from utils import log_graphviz
import sys
def vip_init(args):
    create_repository(args.path)

def vip_cat_file(args):
    repository = repository_find()
    cat_file(repository, args.object, fmt=args.type.encode())

def cat_file(repository, repository_object, fmt=None):
    repository_object = read_object(repository,
                                    find_object(repository, repository_object, fmt=fmt))
    sys.stdout.buffer.write(repository_object.serialize())

def vip_log(args):
    repository = repository_find()

    print("DiGraph viper-log{")
    print(" node[shape=rect]")
    log_graphviz(repository, find_object(repository, args.commit), set())
