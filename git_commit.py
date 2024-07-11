from utils import parse_commit
class GitCommit(GitObject):
    _format = b'commit'

    def deserialize(self, data):
        self.kv_map = parse_commit(data)

    def serialize(self):
        return parse_commit(self.kv_map)

    def init(self):
        self.kv_map = dict()
