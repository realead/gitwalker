import gwlib.processcall as pc
from gwlib.gerror import GitWalkerError

class Executor:
    def __init__(self, path):
        self.path=path
    
    def __call__(self):
        if self.path.endswith(".sh"):
            result=pc.execute_process(["sh", self.path], ok_code=[0,1])
        elif self.path.endswith(".py"):
            result=pc.execute_process(["python", self.path], ok_code=[0,1])
        else:
            raise GitWalkerError("Unknown script language. Only *.sh and *.py can be processed")
               
        if result.returncode==0:
            return True
        return False

import argparse

parser = argparse.ArgumentParser(description='automatization of git branches traversals')
parser.add_argument('-g', type=str, required=True,
                    help='path to git repository')
parser.add_argument('-s', type=str, required=True,
                    help='script which should be executed')
parser.add_argument('-b', type=str, default=None,
                    help='name of the branch which should be traversed, either the name of the branch or first/last commit-pair must be specified')
parser.add_argument('-f', type=str, default=None,
                    help='hash of the first commit, either first/last commit-pair or branch name must be specified')
parser.add_argument('-l', type=str, default=None,
                    help='hash of the last commit, either first/last commit-pair or branch name must be specified')
parser.add_argument('-a', type=str, default="verify", choices=set(["verify", "binsearch", "foreach"]),
                    help='name of the action which should be performed, verify being default value ')
parser.add_argument('-V', '--version', 
                    action='version',                    
                    version='%(prog)s (version 0.1)')
                                        
args = parser.parse_args()

import sys
import gwlib.grepo as gitrep
from gwlib.grunner import GitBranchRunner

try:
    #obtaining the view of the branch:
    if args.b is not None:
         if args.f is not None or args.l is not None:
            print >>  sys.stderr, "if branch name is given, start and end commits must not be given"
            exit(2)
         view=gitrep.get_original_branch_view(args.g, args.b)
    else:
        if args.f is None or args.l is None:
           print >>  sys.stderr, "if branch name is not given, both start and end commits must be given"
           exit(2)
        view=gitrep.get_subbranch_view(args.g, args.f, args.l)
            

    #run the walker
    runner=GitBranchRunner(view)

    exe=Executor(args.s)
    if args.a=="verify":
        bad_hashes=runner.verify_each_commit(exe)
        if bad_hashes:
            print "\n".join([bad.get_hash_value()+":"+bad.get_title() for bad in bad_hashes])
            exit(1)
    elif args.a=="foreach":
        bad_hashes=runner.verify_each_commit(exe, stop_at_first_error=True)
        if bad_hashes:
            bad=bad_hashes[0]
            print bad.get_hash_value()+":"+bad.get_title()
            exit(1)
    elif args.a=="binsearch":
        bad_hash=runner.bin_search(exe)
        print "broken with commit:", bad_hash.get_hash_value(),":", bad_hash.get_title()
    else:
        print >> sys.stderr, "not implemented action", args.a
        exit(2)               
    
except GitWalkerError as e:
    print >> sys.stderr, "Error:", e.message
    exit(2)  
           
