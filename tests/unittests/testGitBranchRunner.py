import unittest

import sys
sys.path.append('../src')

from gwlib.grepo import get_original_branch_view as gbv
from gwlib.grepo import GitRepository
from gwlib.grunner import GitBranchRunner
from gwlib.gerror import GitWalkerError


import os.path
import sh

def fileC_exists():
    return os.path.isfile("../testrep/fileC.txt") 
    
def fileD_exists():
    return os.path.isfile("../testrep/fileD.txt") 
    
class ShExistenceChecker:
    def __init__(self, file_path):
        self.path=file_path
        
    def __call__(self):
        output=sh.sh(["-x", "scripts/check_file_exists.sh", self.path], _ok_code=[0,1])
        if output.exit_code==0:
            return True
        return False
       
class GitBranchRunnerTesterBranchC(unittest.TestCase):
    def setUp(self):
        self.runner=GitBranchRunner(gbv('../testrep', "fileC"))
    
    @classmethod
    def tearDownClass(cls):
        git=GitRepository('../testrep')
        git.checkout("master")
        
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
        with self.assertRaises(GitWalkerError) as context:
            self.runner.bin_search(checker) 
        self.assertTrue('Already the base is broken, cannot do binary search' in context.exception)
      
      
       
       
class ShTextNotExistsChecker:
    def __init__(self, file_path, searched_string):
        self.path=file_path
        self.string=searched_string
        
    def __call__(self):
        output=sh.sh(["scripts/line_in_file_exists.sh", self.path, self.string], _ok_code=[0,1])
        if output.exit_code==0:
            return False
        return True       
       
class GitBranchRunnerTesterBranchAnotherA(unittest.TestCase):
    def setUp(self):
        self.runner=GitBranchRunner(gbv('../testrep', "another_fileA"))
        
    @classmethod
    def tearDownClass(cls):
        git=GitRepository('../testrep')
        git.checkout("master")
    
    
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
        
                  
             
