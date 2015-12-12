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

Definitions
```
-u, --user:         Usename		(i.e: "John Doe <johndoe@random.com>")  
-p, --permission:   Permission	(i.e: commit, merge, write)  
-s, --start:        Start Time	(i.e: "2015-12-12 00:00:00", true, false)  
-e, --end:          End Time	(i.e: "2015-12-12 00:00:00", true, false)  
-l, --layer:        Layer		(i.e: 0,1,2 or "0 1 2" or 0;1;2)  
-b, --branch:       Branch		(i.e: 0,1,2 or "0 1 2" or 0;1;2)  
```
  
The current system generates a JSON file named "acl.json" which "metadata_lib.py" via "parse_repository.py" will use to run checks against "parse_repository.py"'s metadata dictionary which is also found in "metadata.json".
  
# To Run Totolly Secure's algorithm
Ideally you will have already run "ctrl.py" and have generated an "acl.json" file which will be used in the following steps:
```
python init_and_built.py <Repository URL>
```
Example:
```
python init_and_built.py https://www.github.com/kellender/Totolly-Secure
```
  
A "metadata.json" file should have been created outlining the information about the git tree.  
A "violations.json" file should have been created listing all the commit hashes as keys and an associate string value as errors or warnings about the git tree based on the "acl.json" file which was set before hand. If the string is empty or "", this means there are no errors or warnings.
  
# Metadata Format
```
{
    "a0c23ade1a276d4ea23632f517b179a364a16aaa": {
        "code_reviewed": "False", 
        "child1": "4e5dda2da0884eee83d9383c3ecd589ba2d75b74", 
        "layer": 0, 
        "branch": "master", 
        "committer": "Adrien Duermael <adrien@docker.com>", 
        "author": "Adrien Duermael <adrien@docker.com>", 
        "parent1": "e5a40df975c691cafbdc714d536ff8451e7d9e4c", 
        "commit_type": "commit", 
        "commit_timestamp": "2015-06-24 19:10:02 -0700", 
        "author_timestamp": "2015-06-24 19:10:02 -0700"
    }, 
    "31d005f75223323d72ca3ea1ab8b1875f0f4300a": {
        "code_reviewed": "False", 
        "child1": "25bf67188ecdacbd68f5bfcc1dec74e0fc6a6f9f", 
        "layer": 0, 
        "branch": "master", 
        "committer": "Gaetan de Villele <gdevillele@gmail.com>", 
        "author": "Gaetan de Villele <gdevillele@gmail.com>", 
        "parent1": "dbdcb6c594867e348c3aed82ddb19bc2b5106c7f", 
        "commit_type": "commit", 
        "commit_timestamp": "2015-06-23 13:15:58 -0700", 
        "author_timestamp": "2015-06-23 13:15:58 -0700"
    },
    ...
}
```
  
Definitions
 ```
 "code_reviewed":		Checks whether author's code has been merged by another person
 "childN":				Hash of the next commit in time; if N is greater than 1, there is at least 1 branch or fork
 "layer":				Number of merges away from the master repository a branch is
 "branch":				Unique branch name given to a respository
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
    "Gaetan de Villele <gdevillele@gmail.com>": {
        "write": {
            "start": "1800-12-10 00-00-00", 
            "layer": true, 
            "end": "1900-12-11 00-00-00",
            "branch": true
        }, 
        "merge": {
            "start": "2014-12-01 00-00-00", 
            "layer": [
                "0", 
                "1"
            ], 
            "end": "2014-12-11 00-00-00",
            "branch": true
        }, 
        "commit": {
            "start": "2014-12-01 00-00-00", 
            "layer": [
                "0", 
                "1"
            ], 
            "end": "2014-12-11 00-00-00",
            "branch": true
        }
    },
	"Gaetan <gdevillele@gmail.com>": {
        "write": {
            "start": "1800-12-10 00-00-00", 
            "layer": true, 
            "end": "1900-12-11 00-00-00",
            "branch": true
        }, 
        "merge": {
            "start": "2014-12-01 00-00-00", 
            "layer": [
                "0", 
                "1"
            ], 
            "end": "2014-12-11 00-00-00",
            "branch": true
        }, 
        "commit": {
            "start": "2014-12-01 00-00-00", 
            "layer": [
                "0", 
                "1"
            ], 
            "end": "2014-12-11 00-00-00",
            "branch": true
        }
    }
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
    "a0c23ade1a276d4ea23632f517b179a364a16aaa": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "31d005f75223323d72ca3ea1ab8b1875f0f4300a": "Author Gaetan de Villele <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan de Villele <gdevillele@gmail.com> does not have write permissions in branch master. Committer Gaetan de Villele <gdevillele@gmail.com> committed after permission has expired. Committer Gaetan de Villele <gdevillele@gmail.com> does not have commit permissions in branch master. ", 
    "2ce9a4838446111c5235aa5a340c9c723df9ff1b": "Author Gaetan de Villele <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan de Villele <gdevillele@gmail.com> does not have write permissions in branch master. Committer Gaetan de Villele <gdevillele@gmail.com> committed after permission has expired. Committer Gaetan de Villele <gdevillele@gmail.com> does not have commit permissions in branch master. ", 
    "0d9b22584a658fed061b51eb01ee672025cdaad6": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "c6f38372baa477fac494daedd33eae43019616ca": "Author Gaetan de Villele <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan de Villele <gdevillele@gmail.com> does not have write permissions in branch master. Committer Gaetan de Villele <gdevillele@gmail.com> committed after permission has expired. Committer Gaetan de Villele <gdevillele@gmail.com> does not have commit permissions in branch master. ", 
    "4c255be43182af8bdf8d371e5d2d2b4964f7346e": "Merger Gaetan <gdevillele@gmail.com> merged after permission has expired. Merger Gaetan <gdevillele@gmail.com> does not have merge permissions in branch master. Author Gaetan <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan <gdevillele@gmail.com> does not have write permissions in branch master. ", 
    "943b7b14a3c7aa24b016d3733ca2993f7c0c0cd3": "Merger Gaetan <gdevillele@gmail.com> merged after permission has expired. Merger Gaetan <gdevillele@gmail.com> does not have merge permissions in branch master. Author Gaetan <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan <gdevillele@gmail.com> does not have write permissions in branch master. ", 
    "21a15ed8c902ae889cb3d14490ebfe9ece2a0f80": "Merger Gaetan <gdevillele@gmail.com> merged after permission has expired. Merger Gaetan <gdevillele@gmail.com> does not have merge permissions in branch master. Author Gaetan <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan <gdevillele@gmail.com> does not have write permissions in branch master. ", 
    "eec9594ad1d90227aca54781808d9ad2c7a6e017": "Merger Gaetan <gdevillele@gmail.com> merged after permission has expired. Merger Gaetan <gdevillele@gmail.com> does not have merge permissions in branch master. Author Gaetan <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan <gdevillele@gmail.com> does not have write permissions in branch master. ", 
    "b57b303fd5dfc48b923c7d54324527189a9c3aaa": "Author Gaetan de Villele <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan de Villele <gdevillele@gmail.com> does not have write permissions in branch branch12. Committer Gaetan de Villele <gdevillele@gmail.com> committed after permission has expired. Committer Gaetan de Villele <gdevillele@gmail.com> does not have commit permissions in branch branch12. ", 
    "4a1d156e7256acfac13229497ea0cbc00212136a": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "1d50d516cc5bbc434881ca3bad6c242da6a63f29": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "f98aea6c967c97dd670009a7490c6c5a9a95b845": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. Merger Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "25bf67188ecdacbd68f5bfcc1dec74e0fc6a6f9f": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "fc94aa38f29ccae5108c6318587fc182b79d40b7": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "36aa5f3d50c2a4898cc95cd6a055e45227823294": "Author Dave Tucker <dt@docker.com> not in ACL. Committer Dave Tucker <dt@docker.com> not in ACL. ", 
    "06e5a323c6760762e7de0827cfb8b64a1d17dca2": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "21677b3d21320e39cad304e22604da51f78bf06b": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "43d7a53c7b01a4792ec689c9d720940c765d0f6c": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "22a69a77b2442e668fcff2aa9921e5528016a91b": "Author Dave Tucker <dt@docker.com> not in ACL. Committer Dave Tucker <dt@docker.com> not in ACL. ", 
    "240ed3f035f2603b89eb56dfd93795a63912d5d2": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "fb45be9d7df6ce39f2c2674dabf4f2093802cd59": "Merger Gaetan <gdevillele@gmail.com> merged after permission has expired. Merger Gaetan <gdevillele@gmail.com> does not have merge permissions in branch master. Author Gaetan <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan <gdevillele@gmail.com> does not have write permissions in branch master. ", 
    "9aeba24a6ee5d3be826c55e5fdaf6a16476b223f": "Author Gaetan de Villele <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan de Villele <gdevillele@gmail.com> does not have write permissions in branch master. Committer Gaetan de Villele <gdevillele@gmail.com> committed after permission has expired. Committer Gaetan de Villele <gdevillele@gmail.com> does not have commit permissions in branch master. ", 
    "2922361ada17e9011a43e6d7c47f54b17d14d7d7": "Author Gaetan de Villele <gdevillele@gmail.com> wrote after permission has expired. Author Gaetan de Villele <gdevillele@gmail.com> does not have write permissions in branch master. Committer Gaetan de Villele <gdevillele@gmail.com> committed after permission has expired. Committer Gaetan de Villele <gdevillele@gmail.com> does not have commit permissions in branch master. ", 
    "3c7d74520df2de4873aa21e28b72596aee459556": "Author Dave Tucker <dt@docker.com> not in ACL. Committer Dave Tucker <dt@docker.com> not in ACL. ", 
    "520171a32a84bad7bbd2eb5cc27ab0166b46bbc4": "Author Dave Tucker <dave@dtucker.co.uk> not in ACL. Committer Dave Tucker <dave@dtucker.co.uk> not in ACL. Merger Dave Tucker <dave@dtucker.co.uk> not in ACL. ", 
    "8b2c01eaf9da7de4a4c1fab90c320758fda4c377": "Merge not code reviewed. Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. Merger Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "f1db84acd81744b181192a0a2193e69acb865db5": "Author Adrien Duermael <adrien@docker.com> not in ACL. Committer Adrien Duermael <adrien@docker.com> not in ACL. ", 
    "b6d0e1d074c6540dbc31717203fedc01ab8af7c1": "Author Dave Tucker <dt@docker.com> not in ACL. Committer Dave Tucker <dt@docker.com> not in ACL. ",
  ...
}
```
  
Defintions
```
"<hash>":	Key or Hash of commit from metadata dictionary or metadata.json file
"<string>":	Error string displaying all the errors for that commit based on acl.json file
```
