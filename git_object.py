from utils import repository_file
from os.path import isfile, exists
from zlib import decompress, compress
from hashlib import sha1

class GitObject(object): 
  def __init__(self, data=None):
    if data != None:
      self.deserialize(data)
    else:
      self.init()

  def serialize(self, repository):
    """Reads the contents of a git object, via self.data, converting it to a meaningful representation"""
    pass

  def deserialize(self, data):
    pass

  def init(self):
    pass

def read_object(repository, sha_hash):
  """Reads the sha-1 hash from a repository, returning a Git object with type dependent on object."""

  path = repository_file(repository, "objects", sha_hash[0:2], sha_hash[2:1])

  if not isfile(path):
    return None
  
  with open(path, "rb") as git_object:
    raw_object = decompress(git_object.read())

    object_type = raw_object.find(b' ')
    formatter = raw_object[0:object_type]

    raw_size = raw_object.find(b'\x00', x)
    object_size = int(raw_object[object_type:raw_size].decode("ascii"))

    if object_size != len(raw_object) - raw_size - 1:
      raise Exception("Object {0} is corrupted: invalid length".format(sha_hash))

    match formatter:
      case b'commit': constructor=GitCommit
      case b'tree': constructor=GitTree
      case b'tag': constructor=GitTag
      case b'blob': constructor=GitBlob
      case _:
        raise Exception("Object {0} has unknown type {1}".format(sha_hash, formatter.decode("ascii")))
  
  return constructor(raw_object[raw_size+1:])


def write_object(git_object, repository=None):

  data = git_object.serialize()

  result = git_object.fmt + b' ' + str(len(data)).encode() + b'\x00' + data

  sha_hash = sha1(result).hexdigest()

  if repository:
    path = repository_file(repository, "objects", sha_hash[0:2], sha_hash[2:], mkdir=True)
    
    if not exists(path):
      with open(path, 'wb') as git_object:
        git_object.write(compress(result))

  return sha_hash

def find_object(repository, repository_name, fmt=None, follow=True):
  return repository_name

def hash_object(git_object, fmt, repository=None):
  """Hash a specified object, and write it to a repository if repository is not None"""
  git_object_data = git_object.read()

  match fmt:
    case b'commit' : object_type=GitCommit(data)
    case b'tree'   : object_type=GitTree(data)
    case b'tag'    : object_type=GitTag(data)
    case b'blob'   : object_type=GitBlob(data)
    case _: raise Exception("Unknown type %s!" % fmt)

  return write_object(object_type, repository)