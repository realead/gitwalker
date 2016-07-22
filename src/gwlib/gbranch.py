
       
class GitBranchView:
    def __init__(self, basecommit, branch_commits):
        self.base=basecommit
        self.commits=branch_commits
    
    def get_base(self):
        return self.base
                         
