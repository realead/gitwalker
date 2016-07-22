import sh

class GitWalkerError(Exception):
    pass

from gwlib.gcommit import GitCommit

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
        return [self.get_commit(commit_hash) for commit_hash in reversed(commit_hashes)]
        
            
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
        if self.commits:
            self.base=self.commits[0].get_parent()
        else:
            self.base=None
    
    def __verify_commit(self, commit, verifier):
        commit.checkout()
        return True if verifier() else False  
        
    def verify_each_commit(self, verifier):
        bad_commits=[]
        for commit in self.commits:
            if not self.__verify_commit(commit, verifier):
                bad_commits.append(commit)
                
        return bad_commits
        
    def bin_search(self, verifier):
        if not self.__verify_commit(self.base, verifier):
            raise GitWalkerError("Already the base is broken, cannot do binary search")
        if self.__verify_commit(self.commits[-1], verifier):
            raise GitWalkerError("The last commit is Ok, cannot do binary search")
        is_ok=-1
        is_bad=len(self.commits)-1
        
        while is_bad-is_ok>1:
            next=(is_bad+is_ok)//2
            if self.__verify_commit(self.commits[next], verifier):
                is_ok=next
            else:
                is_bad=next
        
        return self.commits[is_bad]
        
    def get_repository(self):
        return self.rep
                         
