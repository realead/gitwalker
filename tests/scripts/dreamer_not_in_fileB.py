try:
    with open('../testrep/fileB.txt', "r") as f:
        lines=f.readlines()
except Exception:
    exit(0)#not found
       
for li in lines:
    if "You may call me a dreamer!"  in li:
        exit(1)
        
exit(0)


