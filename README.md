# gitwalker
automatization script for git

## About

*GitWalker* can be used for checkout every commit and to execute a script/an operation for every checkout. For example

   1. Check that for every commit build and tests are successful (typically after rebase)
   2. Submitting every commit to another SVN
   3. automatically using bisection to find first bad commit
   
*GitWalker* supports sh- and python-scripts. If the execution of an executable is desirable it must be wrapped in a script.

## Prerequisites
   1. python 2.7
   2. git (tested with 2.9.2, but should work with every git version)
   3. python sh module (https://amoffat.github.io/sh/)

## Usage

The script `gitwalker.py` can be found in folder *src*. For example

    python2.7 gitwalker.py -g path_to_git_rep -s my_script.sh -f start_hash -l end_hash -a verify
    
would checkout every commit in the git repository *path_to_git_rep* starting with commit *start_hash* and ending with commit *end_hash* and call the script *my_script.sh* after every checkout. 

### Specifying commits of interest

   1. Using branch name: all commits which belongs to the specified branch but not to the master, e.g. `-b my_branch_name`
   2. Using first/last commit hash e.g. `-f aaabbbbdd -l 12345667` for choosing all commits from *aaabbbbdd* to *12345667*, inclusive.
   
Either *-b* or both *-f* and *-l* options must be given

### Actions

   1. *verify* - calls the script for every commit of interest, returns the hashes of commits for which the provided script fails (exit code 1)
   2. *foreach* - the same as verify, but stops after the first failure of the script (exit code 1) and returns the hash of the bad commit
   3. *binsearch* - uses binary search to find first bad commit, returns its hash
   
*verify* is the default action.


## Testing:

The tests can be found in folder *tests*. To be able to run the tests the test repository *testrep* which is a submodule of the gitwalker git repository.  For tests to work the following steps should be executed:
   1. `git clone --recursive` or if already cloned:
       a. `git submodule init`
       b. `git submodule update`
   2. run `sh tests/set_up_branches.sh`
   
   
