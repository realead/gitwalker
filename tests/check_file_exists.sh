#option $1

if [ -e $1 ]; then
    exit 0
else
    exit 1
fi

