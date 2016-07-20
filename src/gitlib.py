import sh


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


class GitRepository:
    def __init__(self, path):
        self.git_rep=["-C", path]
    
    
    def __run_command(self, command, capture_output=False):
        #to see why _tty_out=False go to stackoverflow.com/a/36252138/325365 
        call=sh.git(self.git_rep+command, _tty_out=False)
        if capture_output:
            #strip to get rid of \n
            #str to get read of u'...'
            return [str(line.strip()) for line in call]
        
    def get_commit(self, commit_hash):
        return GitCommit(commit_hash, self)
    
    
    def get_branch_commits(self, branch_name):
        command=["log", branch_name, "^master", "--format=%H"]
        commit_hashes=self.__run_command(command, capture_output=True)
        return [self.get_commit(commit_hash) for commit_hash in commit_hashes]
        
            
    def checkout(self, commit_alias):
        self.__run_command(["checkout", commit_alias])
       
        
    def get_commit_titel(self, commit_hash):
        command=["log", "--format=%s", "-n", "1", commit_hash]
        return self.__run_command(command, capture_output=True)[0]
        
        
    def get_status(self):
        command=["status"]
        return self.__run_command(command, capture_output=True)
        
        
    def get_parent_commit(self, commit_hash):
        command=["log", "--format=%P", "-n", "1", commit_hash]
        hash_value=self.__run_command(command, capture_output=True)
        return self.get_commit(hash_value[0])
           

        
       
class GitBranchRunner:
    def __init__(self, path, branch_name):
        self.rep=GitRepository(path) 
        self.commits=self.rep.get_branch_commits(branch_name)
        
        
    def verify_each_commit(self, verifier):
        bad_commits=[]
        for commit in self.commits:
            commit.checkout()
            if not verifier():
                bad_commits.append(commit)
                
        return bad_commits
        
                       
