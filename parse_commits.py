from subprocess import check_output

# hash of the current commit; starts off with HEAD
commit_hash = check_output(["git", "rev-parse", "HEAD"]).strip()

# while we haven't reached the initial commit
while( commit_hash..... ):
    # text of the current git commit object
    current_commit = check_output(
        ["git", "cat-file", "-p", commit_hash]).split("\n")
    
    # grab all parents of the current commit
    parents = filter(
        lambda s: len(s) != 0 and s.find("parent") == 0, current_commit)

