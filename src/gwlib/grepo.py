import sh

from gcommit import GitCommit
from gbranch import GitBranchView

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
    
    
    def get_branch_commits(self, branch_name, base_branch_name="master"):
        command=["log", branch_name, "^"+base_branch_name, "--format=%H"]
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
        
        
        
def get_original_branch_view(path, branch_name, base_branch_name="master"):
    repo=GitRepository(path)
    commits=repo.get_branch_commits(branch_name, base_branch_name)
    base=commits[0].get_parent() if commits else None
    return GitBranchView(base, commits)
               
