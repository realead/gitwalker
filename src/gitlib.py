
from gwlib.grepo import GitRepository

class GitWalkerError(Exception):
    pass           
        
       
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
                         
