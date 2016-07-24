import unittest

import sys
sys.path.append('../src')

from gwlib.grepo import get_original_branch_view as gbv
from gwlib.grepo import GitRepository


class GitCommitTester(unittest.TestCase):
 
    def setUp(self):
        #self.git=gitlib.GitRepository('../.git/modules/testrep')
        self.git=GitRepository('../testrep')
        
    def tearDown(self):
        self.git.checkout("master")
 
          
    def test_commit_hash(self):
        commit=self.git.get_commit('ff668655dce190ec642d3997fcefb37fa4a83dcb')
        self.assertEqual( commit.get_hash_value(), 'ff668655dce190ec642d3997fcefb37fa4a83dcb')


    def test_commit_hash_half(self):
        commit=self.git.get_commit('ff668655dce190ec642')
        self.assertEqual( commit.get_hash_value(), 'ff668655dce190ec642d3997fcefb37fa4a83dcb')
        

    def test_commits_title(self):
        commit=self.git.get_commit('ff668655dce190ec642d3997fcefb37fa4a83dcb')
        self.assertEqual(commit.get_title(), 'Okay. This old tale...')
 

    def test_parent_commit(self):
        commit=self.git.get_commit('ff668655dce190ec642d3997fcefb37fa4a83dcb')
        parent=commit.get_parent()
        self.assertEqual(parent.get_hash_value(), 'a9a2b56fe46fa25b303cb08b24cfee11c0241003')


    def test_parent_first_commit(self):
        commit=self.git.get_commit('d3be8125c4f0f1134ed741c7c212b22e1c79d776')
        self.assertIsNone(commit.get_parent())


             
if __name__ == '__main__':
    unittest.main()
