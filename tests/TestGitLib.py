import unittest
import sh

import sys
sys.path.append('../src')

import imp
gitlib = imp.load_source('gitlib', '../src/gitlib.py')
 
class GitRepositoryTester(unittest.TestCase):
 
    def setUp(self):
        #self.git=gitlib.GitRepository('../.git/modules/testrep')
        self.git=gitlib.GitRepository('../testrep')
    def tearDown(self):
        self.git.checkout("master")
    
    def get_hashes(self, branch_name):
        return [hs.get_hash_value() for hs in self.git.get_branch_commits(branch_name)]
          
    def test_empty_fileB_branch(self):
        self.assertEqual( self.get_hashes("fileB"), [])


    def test_commits_afA(self):
        expected=['9383283b251a8497ec90a7bb13ddd188518d8572',
                                                             '704c0a1c4a2a1db2eac3be198e11f0873b72b451',
                                                             'ff668655dce190ec642d3997fcefb37fa4a83dcb',
                                                             'a9a2b56fe46fa25b303cb08b24cfee11c0241003',
                                                             'fad7f7ff132f547deb60e56c10d275fac63d7e1d']
        expected.reverse()  
        self.assertEqual( self.get_hashes("another_fileA"), expected)
        
    def test_commits_afB(self):
        expected=['5f7cef49c21e7f8673db5f4663a8ae4784674902',
                                                                 'efa218e67b784161590f9cdd5bc61b1eaf527551',
                                                                 '026176a9fccbe01acd1995fc26db7aa1ae6e8297',
                                                                 '83a345517f68a451cedd56e7373a8436f6645e4c',
                                                                 '97b8bf131de4ebca95b9582ec8eba6133926d43b',
                                                                 'd10b346013a78e8c3e1240c65ede255c50b02f9f']
        expected.reverse()  
        self.assertEqual( self.get_hashes("alternative_fileB"), expected)
                
    def test_commits_fC(self):
        self.assertEqual( self.get_hashes("fileC"), ['1b72d3488b61253587310e835cb3f1f82079b0e2', 'de94a66ae05b41c65bf2174ba52eb65128205732'])

 
 
    def test_get_commit_titel_5f7cef49_from_afB(self):
        self.assertEqual( self.git.get_commit_titel('5f7cef49'), "You know me real good")
        
  
    def test_get_commit_titel_8edae24a6_from_master(self):
        self.assertEqual( self.git.get_commit_titel('8edae24a6668acbf59192c514319b54f47c97943'), "line 17 for fileA")
        
    
    def test_get_parent(self):
        commit=self.git.get_parent_commit('8edae24a6668acbf59192c514319b54f47c97943')
        self.assertEqual(commit.get_hash_value(), "0a717df9574d236e33d167cdee189f36653aaa73")
        

class GitCommitTester(unittest.TestCase):
 
    def setUp(self):
        #self.git=gitlib.GitRepository('../.git/modules/testrep')
        self.git=gitlib.GitRepository('../testrep')
        self.commit=self.git.get_commit('ff668655dce190ec642d3997fcefb37fa4a83dcb')
        
    def tearDown(self):
        self.git.checkout("master")
 
          
    def test_commit_hash(self):
        self.assertEqual( self.commit.get_hash_value(), 'ff668655dce190ec642d3997fcefb37fa4a83dcb')


    def test_commits_title(self):
        self.assertEqual(self.commit.get_title(), 'Okay. This old tale...')
 

    def test_parent_commit(self):
        parent=self.commit.get_parent()
        self.assertEqual(parent.get_hash_value(), 'a9a2b56fe46fa25b303cb08b24cfee11c0241003')




import os.path
def fileC_exists():
    return os.path.isfile("../testrep/fileC.txt") 
    
def fileD_exists():
    return os.path.isfile("../testrep/fileD.txt") 
    
class ShExistenceChecker:
    def __init__(self, file_path):
        self.path=file_path
        
    def __call__(self):
        output=sh.sh(["-x", "check_file_exists.sh", self.path], _ok_code=[0,1])
        if output.exit_code==0:
            return True
        return False
       
class GitBranchRunnerTesterBranchC(unittest.TestCase):
    def setUp(self):
        self.runner=gitlib.GitBranchRunner('../testrep', "fileC")
    def tearDown(self):
        self.runner.get_repository().checkout("master")
        
    def test_verify_fileC_exists(self):
        bad_commits=self.runner.verify_each_commit(fileC_exists)
        self.assertEqual(bad_commits, [])

    def test_verify_fileC_exists2(self):
        checker=ShExistenceChecker("../testrep/fileC.txt")
        bad_commits=self.runner.verify_each_commit(checker)
        self.assertEqual(bad_commits, [])

    def test_verify_fileD_exists(self):
        bad_commits=self.runner.verify_each_commit(fileD_exists)
        self.assertEqual(len(bad_commits), 2)  
                    
    def test_verify_fileD_exists2(self):
        checker=ShExistenceChecker("../testrep/fileD.txt")
        bad_commits=self.runner.verify_each_commit(checker)
        self.assertEqual(len(bad_commits), 2) 
        
    def test_bin_search_fileD(self):
        checker=ShExistenceChecker("../testrep/fileD.txt")
        #self.assertRaises(gitlib.GitWalkerError, self.runner.bin_search, checker)
        with self.assertRaises(gitlib.GitWalkerError) as context:
            self.runner.bin_search(checker) 
        self.assertTrue('Already the base is broken, cannot do binary search' in context.exception)
      
      
       
       
class ShTextNotExistsChecker:
    def __init__(self, file_path, searched_string):
        self.path=file_path
        self.string=searched_string
        
    def __call__(self):
        output=sh.sh(["line_in_file_exists.sh", self.path, self.string], _ok_code=[0,1])
        if output.exit_code==0:
            return False
        return True       
       
class GitBranchRunnerTesterBranchAnotherA(unittest.TestCase):
    def setUp(self):
        self.runner=gitlib.GitBranchRunner('../testrep', "another_fileA")
    def tearDown(self):
        self.runner.get_repository().checkout("master")
    
    
    def get_hash_values(self, checker):
        bad_commits=self.runner.verify_each_commit(checker)
        return [com.get_hash_value() for com in bad_commits]
        
        
    def test_verify_line_nonexisting(self):
        checker=ShTextNotExistsChecker("../testrep/fileA.txt", "The night is dark and full of terror!")
        bad_commits=self.get_hash_values(checker)
        self.assertEqual(bad_commits, ['ff668655dce190ec642d3997fcefb37fa4a83dcb',
                                       '704c0a1c4a2a1db2eac3be198e11f0873b72b451',
                                       '9383283b251a8497ec90a7bb13ddd188518d8572'
                                       ])
 
    def test_verify_line_not_there(self):
        checker=ShTextNotExistsChecker("../testrep/fileA.txt", "I do not exist")
        bad_commits=self.runner.verify_each_commit(checker)
        self.assertEqual(bad_commits, [])        
        
        
            
    def test_bin_search(self):
        checker=ShTextNotExistsChecker("../testrep/fileA.txt", "The night is dark and full of terror!")
        bad_commit=self.runner.bin_search(checker).get_hash_value()
        self.assertEqual(bad_commit, 'ff668655dce190ec642d3997fcefb37fa4a83dcb')
        
                  
             
if __name__ == '__main__':
    unittest.main()
