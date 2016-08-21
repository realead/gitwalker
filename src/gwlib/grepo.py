import processcall as pc

from gcommit import GitCommit
from gbranch import GitBranchView
from gerror import GitWalkerError

    
class GitRepository:
    def __init__(self, path):
        self.git_rep=["-C", path]
    
    
    def __run_command(self, command, capture_output=False):
        output=pc.execute_process(["git"]+self.git_rep+command).stdout
        if capture_output:
            lines=output.split("\n")
            return [line.strip() for line in lines if line]
        
    def get_commit(self, commit_hash):
        if commit_hash:
            return GitCommit(commit_hash, self)
        else:
            return None
    
    
    def get_branch_commits(self, branch_name, base_branch_name="master"):
        command=["log", branch_name, "^"+base_branch_name, "--format=%H"]
        commit_hashes=self.__run_command(command, capture_output=True)
        return [self.get_commit(commit_hash) for commit_hash in reversed(commit_hashes)]
        
            
    def checkout(self, commit_alias):
        self.__run_command(["checkout", commit_alias])
       
    def get_commit_hash(self, commit_hash):
        command=["log", "--format=%H", "-n", "1", commit_hash]
        return self.__run_command(command, capture_output=True)[0]  
        
    def get_commit_titel(self, commit_hash):
        command=["log", "--format=%s", "-n", "1", commit_hash]
        return self.__run_command(command, capture_output=True)[0]     
        
    def get_status(self):
        command=["status"]
        return self.__run_command(command, capture_output=True)
        
        
    def get_parent_commit(self, commit_hash):
        command=["log", "--format=%P", "-n", "1", commit_hash]
        parent_hashes=self.__run_command(command, capture_output=True)
        if parent_hashes:
            first_parent_hash=parent_hashes[0].split()[0]#for merged commit take just the first parent
        else:
            first_parent_hash=""
        return self.get_commit(first_parent_hash)
        
        
        
def get_original_branch_view(path, branch_name, base_branch_name="master"):
    repo=GitRepository(path)
    commits=repo.get_branch_commits(branch_name, base_branch_name)
    return GitBranchView(commits)
    
def get_subbranch_view(path, first_hash, last_hash):
    repo=GitRepository(path)
    commits=[]
    
    first_commit=repo.get_commit(first_hash)
    current_commit=repo.get_commit(last_hash)    
    while True:
        if current_commit is None:
            raise GitWalkerError("first_hash is not a predecessor of the last_hash")
        commits.append(current_commit)
        if current_commit.get_hash_value()==first_commit.get_hash_value():
            break
        current_commit=current_commit.get_parent()
    commits.reverse()
    return GitBranchView(commits)
               
