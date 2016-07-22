

class GitCommit:
    def __init__(self, commit_hash, repository):
        self.__commit_hash=commit_hash
        self.__rep=repository
        self.__title=self.__rep.get_commit_titel(commit_hash)
        
    def to_string(self, hash_len=7):
        return self.__commit_hash[:hash_len]+"\t"+self.__title
        
    def checkout(self):
        return self.__rep.checkout(self.__commit_hash)

    def get_hash_value(self):
        return self.__commit_hash
    
    def get_title(self):
        return  self.__title
    
    def get_parent(self):
        return  self.__rep.get_parent_commit(self.__commit_hash)
        
        
