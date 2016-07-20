#option $1 - file name
#option $2 - string to search for

if grep -q "$2" "$1"; then
   exit 0
else
   exit 1
fi

