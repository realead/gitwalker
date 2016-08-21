

PATTERN=${1:-test*.py}
python -m unittest discover -s unittests -p $PATTERN

