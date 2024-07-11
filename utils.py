from os.path import join, exists, isdir
from os import makedirs
from collections import OrderedDict

from git_object import read_object
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

def serialize_commit(kv_map):
    return_value = b''

    for key in kv_map.keys():
        if key == None: continue

        value = kv_map[key]

        if type(value) != list:
            value = [ value ]

        for element in value:
            return_value += key + b' ' + (value.replace(b'\n', b'\n ')) + b'\n'

    return_value += b'\n' + kv_map[None] + b'\n'

    return return_value

def log_graphviz(repo, sha, seen):

    if sha in seen:
        return
    seen.add(sha)

    commit = read_object(repo, sha)
    short_hash = sha[0:8]
    message = commit.kvlm[None].decode("utf8").strip()
    message = message.replace("\\", "\\\\")
    message = message.replace("\"", "\\\"")

    if "\n" in message: # Keep only the first line
        message = message[:message.index("\n")]

    print("  c_{0} [label=\"{1}: {2}\"]".format(sha, sha[0:7], message))
    assert commit.fmt==b'commit'

    if not b'parent' in commit.kvlm.keys():
        # Base case: the initial commit.
        return

    parents = commit.kvlm[b'parent']

    if type(parents) != list:
        parents = [ parents ]

    for p in parents:
        p = p.decode("ascii")
        print ("  c_{0} -> c_{1};".format(sha, p))
        log_graphviz(repo, p, seen)
