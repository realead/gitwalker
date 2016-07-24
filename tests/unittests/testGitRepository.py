import unittest

import sys
sys.path.append('../src')

import gwlib.grepo
from gwlib.grepo import GitRepository
from gwlib.gerror import GitWalkerError

 
class GitRepositoryTester(unittest.TestCase):
 
    def setUp(self):
        #self.git=gitlib.GitRepository('../.git/modules/testrep')
        self.git=GitRepository('../testrep')
    def tearDown(self):
        self.git.checkout("master")
    
    def get_hashes(self, branch_name):
        view=gwlib.grepo.get_original_branch_view('../testrep', branch_name)
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

 
 
    def test_get_commit_titel_5f7cef49_from_afB(self):
        self.assertEqual( self.git.get_commit_titel('5f7cef49'), "You know me real good")
        
  
    def test_get_commit_titel_8edae24a6_from_master(self):
        self.assertEqual( self.git.get_commit_titel('8edae24a6668acbf59192c514319b54f47c97943'), "line 17 for fileA")
        
    
    def test_get_parent(self):
        commit=self.git.get_parent_commit('8edae24a6668acbf59192c514319b54f47c97943')
        self.assertEqual(commit.get_hash_value(), "0a717df9574d236e33d167cdee189f36653aaa73")
        
        
    def test_get_subbranch_view(self):
        view=gwlib.grepo.get_subbranch_view('../testrep', 'd3be8125c4f0f1134ed741c7c212b22e1c79d776', '026176a9fccbe01acd1995fc26db7aa1ae6e8297')
        self.assertIsNone(view.get_base())
        hashes=[hs.get_hash_value() for hs in view.commits]
        expected=  ['d3be8125c4f0f1134ed741c7c212b22e1c79d776',
                    '74ef69cfef270cba65e5f98cca1070fd8d78918c',
                    '32bb13022ed7575888692d911ec211e6b4e0caca',
                    'bf280808044c93ceb1c97dcc90cd8e113159a127',
                    '0a717df9574d236e33d167cdee189f36653aaa73',
                    '8edae24a6668acbf59192c514319b54f47c97943',
                    'd10b346013a78e8c3e1240c65ede255c50b02f9f',
                    '97b8bf131de4ebca95b9582ec8eba6133926d43b',
                    '83a345517f68a451cedd56e7373a8436f6645e4c',
                    '026176a9fccbe01acd1995fc26db7aa1ae6e8297']
        self.assertEqual(hashes, expected)

     
    def test_get_subbranch_view_halfhash(self):
        view=gwlib.grepo.get_subbranch_view('../testrep', 'd3be8125c4f0f1134ed741c7c212b22e1c79', '026176a9fccbe01acd1995fc26db7aa1ae6e829')
        self.assertIsNone(view.get_base())
        hashes=[hs.get_hash_value() for hs in view.commits]
        expected=  ['d3be8125c4f0f1134ed741c7c212b22e1c79d776',
                    '74ef69cfef270cba65e5f98cca1070fd8d78918c',
                    '32bb13022ed7575888692d911ec211e6b4e0caca',
                    'bf280808044c93ceb1c97dcc90cd8e113159a127',
                    '0a717df9574d236e33d167cdee189f36653aaa73',
                    '8edae24a6668acbf59192c514319b54f47c97943',
                    'd10b346013a78e8c3e1240c65ede255c50b02f9f',
                    '97b8bf131de4ebca95b9582ec8eba6133926d43b',
                    '83a345517f68a451cedd56e7373a8436f6645e4c',
                    '026176a9fccbe01acd1995fc26db7aa1ae6e8297']
        self.assertEqual(hashes, expected)   
        
    def test_get_subbranch_view_wrong(self):
        with self.assertRaises(GitWalkerError) as context:
            gwlib.grepo.get_subbranch_view('../testrep', 'ff668655dce190ec642d3997fcefb37fa4a83dcb', '1b72d3488b61253587310e835cb3f1f82079b0e2')
        
        self.assertEqual("first_hash is not a predecessor of the last_hash", context.exception.message)
        
        
              

if __name__ == '__main__':
    unittest.main()
