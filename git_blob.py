from git_object import GitOjbect

class GitBlob(GitObject):
    fmt = b'blob'

    def serialize(self):
        return self.blob_data
    
    def deserialize(self, data):
        self.blob_data = data