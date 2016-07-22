
       
class GitBranchView:
    def __init__(self, branch_commits):
        self.base=branch_commits[0].get_parent() if branch_commits else None
        self.commits=branch_commits
    
    def get_base(self):
        return self.base
                         
