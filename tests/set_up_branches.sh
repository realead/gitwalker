
my_dirname=$(dirname $0)
git_rep_path="$my_dirname/../testrep"

##checkout branches of interest, tracking will be set up automaticly 
(cd $git_rep_path && pwd && git checkout fileB)
(cd $git_rep_path && pwd && git checkout alternative_fileB)
(cd $git_rep_path && pwd && git checkout another_fileA)
(cd $git_rep_path && pwd && git checkout fileC)

###restore back to master:
(cd $git_rep_path && pwd && git checkout master)

