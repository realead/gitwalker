import unittest

import sys
sys.path.append('../src')

from gwlib.grepo import get_original_branch_view as gbv
from gwlib.grepo import GitRepository

 
class GitBranchViewTester(unittest.TestCase):
        
    @classmethod
    def tearDownClass(cls):
        git=GitRepository('../testrep')
        git.checkout("master")
    
    def get_hashes(self, branch_name):
        view=gbv('../testrep', branch_name)
        return [hs.get_hash_value() for hs in view.commits]
          
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

 
        
             
if __name__ == '__main__':
    unittest.main()
