
GIT_WALKER="python2.7 ../src/gitwalker.py"
GIT_REP="../testrep"

test_cnt=0
failed_test_cnt=0


verify_error_output(){
    OPTIONS="$1"
    EXPECTED=$(echo "$2")
    ERROR_MESSAGE=$($GIT_WALKER -g $GIT_REP $OPTIONS 2>&1 1>/dev/null)
    
    if [ "$ERROR_MESSAGE" != "$EXPECTED" ]; then
        echo "Error in $3: expected [$EXPECTED] vs [$ERROR_MESSAGE]"
        failed_test_cnt=$((failed_test_cnt+1))
    fi
    test_cnt=$((test_cnt+1))

}

verify_std_output(){
    OPTIONS="$1"
    EXPECTED=$(echo "$2")
    OUTPUT=$($GIT_WALKER -g $GIT_REP $OPTIONS)
    
    if [ "$OUTPUT" != "$EXPECTED" ]; then
        echo "Error in $3: expected [$EXPECTED] vs [$OUTPUT]"
        failed_test_cnt=$((failed_test_cnt+1))
    fi
    test_cnt=$((test_cnt+1))

}


#test cases:

## wrong inputs
verify_error_output "-s scripts/dreamer_not_in_fileB.sh" "if branch name is not given, both start and end commits must be given" no_view_given
verify_error_output "-s scripts/dreamer_not_in_fileB.sh -b fileB -f 3412322" "if branch name is given, start and end commits must not be given" branch_and_first_given
verify_error_output "-s scripts/dreamer_not_in_fileB.sh -b fileB -l 3412322" "if branch name is given, start and end commits must not be given" branch_and_last_given
verify_error_output "-s scripts/dreamer_not_in_fileB.sh -f 3412322" "if branch name is not given, both start and end commits must be given" only_first_given
verify_error_output "-s scripts/dreamer_not_in_fileB.sh -l 3412322" "if branch name is not given, both start and end commits must be given" only_last_given



## verify 
verify_std_output "-s scripts/dreamer_not_in_fileB.sh -b alternative_fileB" "83a345517f68a451cedd56e7373a8436f6645e4c:actually I did\n026176a9fccbe01acd1995fc26db7aa1ae6e8297:I would rather prefer the beatles\nefa218e67b784161590f9cdd5bc61b1eaf527551:not my favorite, but why not?\n5f7cef49c21e7f8673db5f4663a8ae4784674902:You know me real good" verify_branch_afB 

verify_std_output "-s scripts/dreamer_not_in_fileB.sh -f d3be8125c4f -l 83a345517f6" "83a345517f68a451cedd56e7373a8436f6645e4c:actually I did" verify_last_commit_broken 

verify_std_output "-s scripts/dreamer_not_in_fileB.sh -f 97b8bf131de4 -l 026176a9fccb" "83a345517f68a451cedd56e7373a8436f6645e4c:actually I did\n026176a9fccbe01acd1995fc26db7aa1ae6e8297:I would rather prefer the beatles" verify_two_last_broken 



## binsearch:

verify_std_output "-s scripts/dreamer_not_in_fileB.sh -b alternative_fileB  -a binsearch" "broken with commit: 83a345517f68a451cedd56e7373a8436f6645e4c : actually I did" binsearch_branch_afB 
verify_std_output "-s scripts/dreamer_not_in_fileB.sh -f d3be8125c4f -l 83a345517f6  -a binsearch" "broken with commit: 83a345517f68a451cedd56e7373a8436f6645e4c : actually I did" binsearch_last_commit_broken 
verify_std_output "-s scripts/dreamer_not_in_fileB.sh -f 97b8bf131de4 -l 026176a9fccb -a binsearch" "broken with commit: 83a345517f68a451cedd56e7373a8436f6645e4c : actually I did" binsearch_two_last_broken 








#report:

if [ $failed_test_cnt = "0" ]; then
    echo "$test_cnt tests OK"
else
    echo "$failed_test_cnt out of $test_cnt failed"
    exit 1
fi
