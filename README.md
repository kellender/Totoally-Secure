# Totolly-Secure
Totolly Secure is a VCS checker. The goal is to enforce code review without making too many changes to the current workflow. Also, Totolly Secure will check if commits were properly signed, and attempt to verify the signatures.

# To Run ctrl.py
To get help:
```
python ctrl.py -h
```

To empty permissions JSON file:
```
python ctrl.py -f
```

To delete permissions:
```
python ctrl.py -d <username>
python ctrl.py -d <username> -p <permission>
```

To add permissions:
```
python ctrl.py -u <username> -p <permission> -s <YYYY-MM-DD HH-MM-SS> -e <YYYY-MM-DD HH-MM-SS> -l <#,#,#,...> -b <#,#,#,...>
python ctrl.py -u <username> -p <permission> -s <bool> -e <bool> -l <bool> -b <bool>
```

Example:
```
python ctrl.py -u "John Doe <johndoe@random.com>" -p merge -s "2015-12-12 00:00:00" -e true -l 0,1 -b "0 1 2"
```

# Definitions
-u, --user:        Usename (i.e: "John Doe <johndoe@random.com>")  
-p, --permission:        Permission (i.e: commit merge, write)  
-s, --start:        Start Time (i.e: "2015-12-12 00:00:00", true, false)  
-e, --end:        End Time (i.e: "2015-12-12 00:00:00", true, false)  
-l, --layer:        Layer (i.e: 0,1,2 or "0 1 2" or 0;1;2)  
-b, --branch:        Branch (i.e: 0,1,2 or "0 1 2" or 0;1;2)  
  
The current system generates a JSON file named "acl.json" which "metadata_lib.py" via "parse_repository.py" will use to run checks against "parse_repository.py"'s metadata dictionary which is also found in "metadata.json".
