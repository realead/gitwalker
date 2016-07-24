

python -m unittest discover -s unittests


#verify branch:
GIT_WALKER="python2.7 ../src/gitwalker.py"
GIT_REP="../testrep"
$GIT_WALKER -g $GIT_REP -s scripts/dreamer_not_in_fileB.sh
