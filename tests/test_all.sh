

echo "TESTING FRONT END:"
sh test_front_end.sh

echo "\n\n\nRUNNING UNIT TESTS:"
python -m unittest discover -s unittests


