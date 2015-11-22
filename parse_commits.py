from subprocess import check_output

# hash of the HEAD commit
head = check_output(["git", "rev-parse", "HEAD"]).strip()
traverse( head )

# hashes of commits that were already touched
hashes = []
hashes.add( head )

# Recurse thought the tree until the initial commit is reached.
def traverse( commit_hash ):
    # text of the current git commit object
    current_commit = check_output(
        ["git", "cat-file", "-p", commit_hash]).split("\n")
    
    # parents of the current commit
    parents = []

    # find all parents of the current commit
    for line in current_commit:
        if ( len( line ) != 0 ) and ( line.find( "parent" ) == 0 ):
            parents.add( line )

    if len(parents) == 0:
        # no parents means that the first commit of the branch was reached
        break
    else:
        for parent in parents:
            # parent is in form "parent <hash>"
            parent_hash = parent.split()[1]

            if parent_hash not in hashes:
                global hashes

                hashes.add(parent_hash)
                traverse(parent_hash)
