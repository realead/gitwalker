
from grepo import GitRepository
from gbranch import GitBranchView
from gerror import GitWalkerError
    
       
class GitBranchRunner:
    def __init__(self, branch_view):
        self.view=branch_view
    
    def __verify_commit(self, commit, verifier):
        commit.checkout()
        return True if verifier() else False  
        
    def verify_each_commit(self, verifier):
        bad_commits=[]
        for commit in self.view.commits:
            if not self.__verify_commit(commit, verifier):
                bad_commits.append(commit)
                
        return bad_commits
        
    def bin_search(self, verifier):
        #start of the searched range:
        base=self.view.get_base()
        if base is None:
            if self.__verify_commit(self.view.commits[0], verifier):
                is_ok=0
            else:
                return self.view.commits[0]
        else:
            if not self.__verify_commit(self.view.get_base(), verifier):
                raise GitWalkerError("Already the base is broken, cannot do binary search")
            is_ok=-1
            
        #end of the searched range:  
        if self.__verify_commit(self.view.commits[-1], verifier):
            raise GitWalkerError("The last commit is Ok, cannot do binary search")
        is_bad=len(self.view.commits)-1
        
        while is_bad-is_ok>1:
            next=(is_bad+is_ok)//2
            if self.__verify_commit(self.view.commits[next], verifier):
                is_ok=next
            else:
                is_bad=next
        
        return self.view.commits[is_bad]
        
                         
