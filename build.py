"""
<Program Name>
    build.py
    
<Authors>
    Team Totolly Secure
    
<Started>
    December 2015.

<Purpose>
    Command line tool clone and check repository

<Usage>
    python build.py [option] URL
"""


import subprocess
import os
import sys
import parse_repository
from optparse import OptionParser


def build(path):
     """
    <Purpose>
        Starts build process
    
    <Arguments>
        Path to the repository
    
    <Exceptions>
        None
    
    <Returns>
        None
    """
    os.chdir(path)
    parse_repository.parse_driver()


def clone(value):
    """
    <Purpose>
        Clones give repository
    
    <Arguments>
        URL to repo [-b branch name] [path]
    
    <Exceptions>
        None
    
    <Returns>
        None
    """
    print "Checking out repo from", value, "..."
    git_process = subprocess.Popen("git clone " + value, cwd = os.getcwd(), shell = True, 
       stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    (stdout_data, stderr_data) = git_process.communicate()


    # Git prints all status messages to stderr (!). We check its retval 
    # to see if it performed correctly, and halt the program (giving debug 
    # output) if not.
    if git_process.returncode == 0:
       print "Done!"
    else:
      print "*** Error checking out repo. Git returned status code", git_process.returncode
      print "*** Git messages on stdout: '" + stdout_data + "'."
      print "*** Git messages on stderr: '" + stderr_data + "'."
      print
      print """These errors need to be fixed before the build process can proceed. In 
                doubt, please contact the Seattle development team at 
                seattle-devel@googlegroups.com
                and supply all of the above information. Thank you!
                """


def main(args):
    usage = "usage: %prog [option] repository.gitlink"
    parser = OptionParser(usage)


    parser.add_option("-b", "--Branch", dest="branch",
            default=None, action = "store", type="string",
            help="Clones a specific branch of a repository", metavar="repository")

    parser.add_option("-p", "--Path", dest="path",
            default=None, action = "store", type="string",
            help="Stores the cloned repostiory in this path", metavar="repository")


    (options, args) = parser.parse_args()

    clone_param = args[0]
    path = None
    repo = args[0]
    for key, value in options.__dict__.items():
        if(key == 'branch' and value != None):
            clone_param += " -b " + value
        if (key == 'path' and value != None):
            clone_param += " " + value
            path = value

    #if path is not specified then path is taken form the repository        
    if(path == None):
        path = repo.split('/')[-1]

    #checks if path exists!
    if(not os.path.isdir(path)):
        clone(clone_param)
    build(path)



if __name__ == "__main__":
    main(sys.argv)