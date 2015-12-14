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
python ctrl.py -u <username> -p <permission> -s <"YYYY-MM-DD HH-MM-SS"> -e <"YYYY-MM-DD HH-MM-SS"> -l <#,#,#,...> -b <#,#,#,...>
python ctrl.py -u <username> -p <permission> -s <bool> -e <bool> -l <bool> -b <bool>
```

Example:
```
python ctrl.py -u "John Doe <johndoe@random.com>" -p merge -s "2015-12-12 00:00:00" -e true -l 0,1 -b "0 1 2"
python ctrl.py -u "John Doe <johndoe@random.com>" -p commit -s true -e true -l true -b true
python ctrl.py -u "John Doe <johndoe@random.com>" -p write -s true -e true -l 0,1 -b true
python ctrl.py -d "John Doe <johndoe@random.com>" -p merge
python ctrl.py -d "John Doe <johndoe@random.com>"
python ctrl.py -f
```

Definitions
```
-u, --user:         Usename		(i.e: "John Doe <johndoe@random.com>")  
-p, --permission:   Permission	(i.e: commit, merge, write)  
-s, --start:        Start Time	(i.e: "2015-12-12 00:00:00", true, false)  
-e, --end:          End Time	(i.e: "2015-12-12 00:00:00", true, false)  
-l, --layer:        Layer		(i.e: 0,1,2 or "0 1 2" or true or false)  
-b, --branch:       Branch		(i.e: 0,1,2 or "0 1 2" or true or false)  
```
  
The current system generates a JSON file named "acl.json" which "metadata_lib.py" via "parse_repository.py" will use to run checks against "parse_repository.py"'s metadata dictionary which is also found in "metadata.json".
  
# To Run Totolly Secure's Algorithm
Ideally you will have already ran "ctrl.py" and have generated an "acl.json" file which will be used in the following steps:

To get help:
```
python build.py -h
```

To run the build:
```
python build.py <Repository URL>
```

To clone a branch and run:
```
python build.py <Repository URL> -b <some_branch_name>
```

To run the specify a path and run:
```
python build.py <Repository URL> -b <some_branch_name> -p <some_path>
```

Example:
```
python build.py https://www.github.com/kellender/Totolly-Secure
python build.py https://www.github.com/kellender/Totolly-Secure -b Permissions
python build.py https://www.github.com/kellender/Totolly-Secure -b Permissions -p ./Dependencies/Totolly-Secure
```

Definitions
```
-b, --branch:       Branch       (i.e: some_branch_name)  
-p, --path:         Path         (i.e: ./Dependencies/Repository_name)  
```

  
A "metadata.json" file should have been created outlining the information about the git tree.  
A "violations.json" file should have been created listing all the commit hashes as keys and an associate string value as errors or warnings about the git tree based on the "acl.json" file which was set before hand. If the string is empty or "", this means there are no errors or warnings.
  
# Metadata Format
```
{
    "612efb5ded0fc3b417a9e272c62a5d170b18695b": {
        "code_reviewed": "False", 
        "child1": "bf35ff2159f6fe94e763f00c6651994aa520f48d", 
        "layer": 1, 
        "branch": 9, 
        "committer": "Jan Karger <punkerat76@gmail.com>", 
        "author": "Jan Karger <punkerat76@gmail.com>", 
        "parent1": "c703e36c0b3f2dbf910c0a7ddb957a04ec81a9e5", 
        "commit_type": "commit", 
        "commit_timestamp": "2015-11-19 10:37:16 +0100", 
        "author_timestamp": "2015-11-19 10:37:16 +0100"
    }, 
    "19888e6822aed62eb7665a36679262248c9cb1c5": {
        "code_reviewed": "False", 
        "child1": "046b87e06724d22aea61e8e0e5a304c03e1e2ea5", 
        "layer": 0, 
        "branch": 0, 
        "committer": "Benjamin Pasero <benjpas@microsoft.com>", 
        "author": "Benjamin Pasero <benjpas@microsoft.com>", 
        "parent1": "2c7bfe53b26d005af0b1cbb87c675140863f4718", 
        "commit_type": "commit", 
        "commit_timestamp": "2015-11-20 13:00:28 +0100", 
        "author_timestamp": "2015-11-20 13:00:28 +0100"
    }, 
    "6e94b27e06cef23a84fca0aff18b7702dc670014": {
        "code_reviewed": "False", 
        "child1": "cc24139a40632ce4b0b7d124871b5cb86b9be060", 
        "layer": 0, 
        "branch": 0, 
        "committer": "Benjamin Pasero <benjpas@microsoft.com>", 
        "author": "Benjamin Pasero <benjpas@microsoft.com>", 
        "parent1": "01751b055930bb27dc1e0c1ca0599aba19b9c5ff", 
        "commit_type": "commit", 
        "commit_timestamp": "2015-11-20 08:42:27 +0100", 
        "author_timestamp": "2015-11-20 08:42:27 +0100"
    }, 
    "60d10f9ae3b052cbad8a65579f7586d0a883e2ee": {
        "code_reviewed": "False", 
        "child1": "c7db0af7e3b1a20242e0600169b77baebaf16e2f", 
        "layer": 0, 
        "branch": 0, 
        "committer": "Andre Weinand <aweinand@microsoft.com>", 
        "author": "Andre Weinand <aweinand@microsoft.com>", 
        "parent1": "ccc4c18231004e1b7c1c6b7ee50eeb3c5d8d288a", 
        "commit_type": "commit", 
        "commit_timestamp": "2015-11-20 15:34:13 +0100", 
        "author_timestamp": "2015-11-20 15:33:32 +0100"
    }, 
    "2ebf742c9444b23f7daaeebe5e28c708ac33dd95": {
        "code_reviewed": "False", 
        "child1": "1bdaaaea404281f4f248fab70bede7d6ac60e99f", 
        "child2": "a8c6596266df01acd4fac3529091795476f0cec7", 
        "branch": 0, 
        "committer": "Chris Dias <chris@diasfam.com>", 
        "author": "Chris Dias <chris@diasfam.com>", 
        "layer": 0, 
        "parent1": "80299a8d4902cd92354f2525a44de7166d6187ce", 
        "commit_type": "pre-branch/fork", 
        "commit_timestamp": "2015-11-15 21:59:34 +0100", 
        "author_timestamp": "2015-11-15 21:59:34 +0100"
    }, 
    "8f82b037fe9a5e8210dcd345bdb69fba0ff50f81": {
        "code_reviewed": "False", 
        "child1": "ef99de7936d45c4199fa51b5654130dafefabe68", 
        "layer": 0, 
        "branch": 0, 
        "committer": "Martin Aeschlimann <martinae@microsoft.com>", 
        "author": "Martin Aeschlimann <martinae@microsoft.com>", 
        "parent1": "d62a44820f684b5bce629f191e6c53da36acaf3e", 
        "commit_type": "commit", 
        "commit_timestamp": "2015-11-13 18:17:22 +0100", 
        "author_timestamp": "2015-11-13 18:17:22 +0100"
    }, 
    "9159003d6c5b36ece74f2acd401750c7a1778241": {
        "code_reviewed": "True", 
        "child1": "15ddb39bed219c79a0930fca6f32f354d64da17b", 
        "layer": 0, 
        "branch": 0, 
        "committer": "Martin Aeschlimann <martinae@microsoft.com>", 
        "author": "Martin Aeschlimann <martinae@microsoft.com>", 
        "parent2": "f7bd7e8fb3c17ec209d223e5cfa696bfd55064f8", 
        "parent1": "ad5c5295647f4c1b418cb07616ee648faa4e83f1", 
        "commit_type": "merge", 
        "commit_timestamp": "2015-11-20 16:18:02 +0100", 
        "author_timestamp": "2015-11-20 16:18:02 +0100"
    }, 
    "9731e5287c97a08005303359d299ab8ea6d6449e": {
        "code_reviewed": "False", 
        "child1": "b703e6779c1e309cfa5d40e9dbe5d0df4b4eb352", 
        "child2": "0c3603a554578788aec82c4d972bf796b1914c96", 
        "branch": 0, 
        "committer": "Joao Moreno <jomo@microsoft.com>", 
        "author": "Joao Moreno <jomo@microsoft.com>", 
        "layer": 0, 
        "parent1": "a0c6a74e24cce5b673c88cd67382ccbb063ea164", 
        "commit_type": "pre-branch/fork", 
        "commit_timestamp": "2015-11-20 09:24:36 +0100", 
        "author_timestamp": "2015-11-20 09:24:36 +0100"
    },
    ...
}
```
  
Definitions
 ```
 "code_reviewed":		Checks whether author's code has been merged by another person
 "childN":				Hash of the next commit in time; if N is greater than 1, there is at least 1 branch or fork
 "layer":				Number of merges away from the master repository a branch is; 0 is master
 "branch":				Unique branch number given to a respository; 0 is master
 "committer"			Committer that pushed
 "author":				Writer/author/Owner of code
 "parentN":				Hash of previous commit in time, if N is greater than 1, there is at least 1 merge
 "commit_type":			Commit type may be commit (regular update or push), merge, or branch/fork
 "commit_timestamp"		Timestamp for commit being pushed/committed
 "author_timestamp":	Timestamp for written code being pushed/committed
 ```
   
# ACL Format
```
{
    "Martin Aeschlimann <martinae@microsoft.com>": {
        "write": {
            "start": "2015-11-19 00:00:00", 
            "layer": [
                "0", 
                "1", 
                "2"
            ], 
            "end": true, 
            "branch": true
        }, 
        "commit": {
            "start": "2015-11-19 00:00:00", 
            "layer": [
                "0", 
                "1", 
                "2"
            ], 
            "end": true, 
            "branch": true
        }, 
        "merge": {
            "start": "2015-11-19 00:00:00", 
            "layer": [
                "0", 
                "1", 
                "2"
            ], 
            "end": true, 
            "branch": true
        }
    }, 
    "Jan Karger <punkerat76@gmail.com>": {
        "write": {
            "start": "2014-12-01 00-00-00", 
            "layer": [
                "0", 
                "1"
            ], 
            "end": "2015-12-11 00-00-00"
        }, 
        "merge": {
            "start": "2014-12-01 00-00-00", 
            "layer": [
                "0", 
                "1"
            ], 
            "end": "2015-12-11 00-00-00"
        }, 
        "commit": {
            "start": "2014-12-01 00-00-00", 
            "layer": [
                "0", 
                "1"
            ], 
            "end": "2015-12-11 00-00-00"
        }
    },
    ...
}
```
  
Definitions
 ```
 "user":	Name of programmer with an email address appended
 "merge":	Key for dictionary of permissions for merging
 "commit":	Key for dictionary of permissions for commit
 "write":	Key for dictionary of permissions for write
 "start":	Start date when permission grants; if bool value of true, start time is open or ambigious
 "end":		End date when permission expires; if bool value of true, end time is open or ambigious
 "layer":	List of layers that permission grants; if bool value of true, all layers are included or else none are
 "branch":	List of branches that permission grants; if bool value of true, all branches are included or else none are
 ```
   
# Violations Format
```
{
    "612efb5ded0fc3b417a9e272c62a5d170b18695b": "Author Jan Karger <punkerat76@gmail.com> does not have write permissions in branch 9. Committer Jan Karger <punkerat76@gmail.com> does not have commit permissions in branch 9. ", 
    "19888e6822aed62eb7665a36679262248c9cb1c5": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "6e94b27e06cef23a84fca0aff18b7702dc670014": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "60d10f9ae3b052cbad8a65579f7586d0a883e2ee": "Author Andre Weinand <aweinand@microsoft.com> not in ACL. Committer Andre Weinand <aweinand@microsoft.com> not in ACL. ", 
    "2ebf742c9444b23f7daaeebe5e28c708ac33dd95": "Author Chris Dias <chris@diasfam.com> not in ACL. Committer Chris Dias <chris@diasfam.com> not in ACL. ", 
    "8f82b037fe9a5e8210dcd345bdb69fba0ff50f81": "", 
    "9159003d6c5b36ece74f2acd401750c7a1778241": "", 
    "9731e5287c97a08005303359d299ab8ea6d6449e": "Author Joao Moreno <jomo@microsoft.com> not in ACL. Committer Joao Moreno <jomo@microsoft.com> not in ACL. ", 
    "fd1a22b5c643c08ba0cd70d6b2e328021e8bff99": "Author isidor <inikolic@microsoft.com> not in ACL. Committer isidor <inikolic@microsoft.com> not in ACL. ", 
    "783155223d7200ac6e655652a53da08c419871c1": "Author Andre Weinand <aweinand@microsoft.com> not in ACL. Committer Andre Weinand <aweinand@microsoft.com> not in ACL. ", 
    "2c7bfe53b26d005af0b1cbb87c675140863f4718": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "ed9a93cc7272bf29a74d6ff05ef217fa9e0932d9": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "3c12981e6d8693f71ad866e104744de901b1b360": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "38aecbbb5e5e945bee441e7aadede5ac366a0046": "Author isidor <inikolic@microsoft.com> not in ACL. Committer isidor <inikolic@microsoft.com> not in ACL. ", 
    "98f95641290c5822bb01039335f80aca57a0ae23": "Author David Storey <storey.david@gmail.com> not in ACL. Committer David Storey <storey.david@gmail.com> not in ACL. ", 
    "96d34d983d37586d37cafa526ad58fb5464bf166": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "2804413940ea443d0b043c080f9107a6509f689e": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "e32df1933a076a264b6d2748973942c03fac7216": "Author Joao Moreno <jomo@microsoft.com> not in ACL. Committer Joao Moreno <jomo@microsoft.com> not in ACL. ", 
    "bd9d62b882841f2bf40b9da4192757e9e8ddf2da": "Author David Storey <storey.david@gmail.com> not in ACL. Committer David Storey <storey.david@gmail.com> not in ACL. ", 
    "cc9e65cea2d55392071203d5490e809f347efcc6": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "0f09edce0102356ab04f1d9a4f79bd3e6c02330d": "", 
    "078aa5ebddbceb3fe8b5ccf7424b3794dcb6d378": "Author Joao Moreno <mail@joaomoreno.com> not in ACL. Committer Joao Moreno <mail@joaomoreno.com> not in ACL. ", 
    "160d58dba78b9acca7d8f9fb629ae17b496a68a7": "Author Chris Dias <cdias@microsoft.com> not in ACL. Committer Chris Dias <cdias@microsoft.com> not in ACL. ", 
    "95896bbee970629dab05e945f251fff24a968330": "Author Johannes Rieken <johannes.rieken@gmail.com> not in ACL. Committer Johannes Rieken <johannes.rieken@gmail.com> not in ACL. ", 
    "c3094f380d5010a7dd43868a00177a5ff7261124": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "22f05dff89174748b454a802e0bc7e566d885927": "Author Lucas Araujo <lucas.lra@gmail.com> not in ACL. Committer Lucas Araujo <lucas.lra@gmail.com> not in ACL. ", 
    "23a08adfcd02a3692762fa18baab8abb232c16f2": "Author Andrea Grieco <angrieco@users.noreply.github.com> not in ACL. Committer Andrea Grieco <angrieco@users.noreply.github.com> not in ACL. ", 
    "046b87e06724d22aea61e8e0e5a304c03e1e2ea5": "Author Alex Dima <alexdima@microsoft.com> not in ACL. Committer Alex Dima <alexdima@microsoft.com> not in ACL. ", 
    "e6d6c1000edcc12ea1773603f8a4b0a84d2ae8f9": "Author Andre Weinand <aweinand@microsoft.com> not in ACL. Committer Andre Weinand <aweinand@microsoft.com> not in ACL. ", 
    "6b8b6302143a5d3527545f5604a2c1ab8f333d71": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "cd42db0e3ef4ddb0924e61cb9308b81e83d4ccbb": "Author Joao Moreno <jomo@microsoft.com> not in ACL. Committer Joao Moreno <jomo@microsoft.com> not in ACL. ", 
    "c878d1ecb66d93e112c2ca59a435cff80920974f": "Author David Storey <storey.david@gmail.com> not in ACL. Committer David Storey <storey.david@gmail.com> not in ACL. ", 
    "6e5ddd3e7e7fe7e8da3eca11e16b7648752d3fbe": "Author Eduardo Pinho <enet4mikeenet@gmail.com> not in ACL. Committer Eduardo Pinho <enet4mikeenet@gmail.com> not in ACL. ", 
    "2ba926ab440a67796bf43189ccfd2c9b9c414e9c": "", 
    "2b6ba9e3cb5c57170b67623395a008c96bf5ebce": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "9ea2f149581de9a9925a74d973f7c8b5d2408862": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "676dca3521a7e2898c766ce1647c06c9e0d2f02b": "Author Joao Moreno <jomo@microsoft.com> not in ACL. Committer Joao Moreno <jomo@microsoft.com> not in ACL. ", 
    "df479d0a6fa4f3c3d8ba7cb9821f9f35802fe2d7": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "dd9d251b5d43a301e9549a62c5e091ec7a946bd3": "Author Steven Clarke <stevencl@users.noreply.github.com> not in ACL. Committer Steven Clarke <stevencl@users.noreply.github.com> not in ACL. ", 
    "c04030ebb577422405cc709b32363355bc16465b": "Author Chris Dias <chris@diasfam.com> not in ACL. Committer Chris Dias <chris@diasfam.com> not in ACL. ", 
    "300756f300f32cc493a03e2383288c704fd79c4c": "Author isidor <inikolic@microsoft.com> not in ACL. Committer isidor <inikolic@microsoft.com> not in ACL. ", 
    "ed139191d6d17eeca9e9034f49f733e52bbdd8e6": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "7cd8b82c86b7a98cb6962066cbd7ba48ddd24f75": "Author Joao Moreno <mail@joaomoreno.com> not in ACL. Committer Joao Moreno <mail@joaomoreno.com> not in ACL. ", 
    "045e1b6dd4489f63a6af3f1df893a9f32e0e9d17": "Author Johannes Rieken <johannes.rieken@gmail.com> not in ACL. Committer Johannes Rieken <johannes.rieken@gmail.com> not in ACL. ", 
    "b75d17c3f7bd05c0dc341a930e50d36042fa3632": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "2d54b7e0ea86fb9e8c62701c305835b5d118562c": "Author David Storey <storey.david@gmail.com> not in ACL. Committer David Storey <storey.david@gmail.com> not in ACL. ", 
    "4a549a0039d90abc7a685b15d6bcdaf5bef69c65": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "0a2f0cbc5c7ebc4573ba93c7b4c007efb1110856": "Author Benjamin Pasero <benjpas@microsoft.com> not in ACL. Committer Benjamin Pasero <benjpas@microsoft.com> not in ACL. ", 
    "cee002f47d5b7c269213a1f000414743130ba9eb": "Author Chris Dias <cdias@microsoft.com> not in ACL. Committer Chris Dias <cdias@microsoft.com> not in ACL. ",
  ...
}
```
  
Defintions
```
"<hash>":	Key or Hash of commit from metadata dictionary or metadata.json file
"<string>":	Error string displaying all the errors for that commit based on acl.json file
```
