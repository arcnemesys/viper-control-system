from repository import create_repository, repository_find
from git_object import read_object, find_object
import sys
def vip_init(args):
    create_repository(args.path)

def vip_cat_file(args):
    repository = repository_find()
    vip_cat_file(repository, args.object, fmt=args.type.encode())

def cat_file(repository, repository_object, fmt=None):
    repository_object = read_object(repository, 
                                    object_find(repository, repository_object, fmt=fmt))
    sys.stdout.buffer.write(repository_object.serialize())