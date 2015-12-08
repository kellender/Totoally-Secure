#from https://github.com/SeattleTestbed/buildscripts 
#usage python init_and_build.py [workflow option] URL
"""
<Program>
  initialize.py 

<Purpose>
  This script does a ``git clone'' of all the dependent repositories
  of a Seattle component.

<Usage>
  * Clone the repository you would like to build on your machine, e.g. using 
      ``git clone https://github.com/SeattleTestbed/seash''
  * Change into the ``scripts'' subdirectory
  * Run this script: 
      ``python initialize.py''
  * The dependencies will be checked out into ``../DEPENDENCIES''.

<Note>
  While this file is redistributed with every buildable Seattle repo, 
  the ``master copy'' (and thus the most up-to-date version) is kept 
  at https://github.com/SeattleTestbed/buildscripts
"""

import subprocess
import os
import sys
import parse_repository
from optparse import OptionParser

def main(args):
  usage = "usage: %prog [option] repository.gitlink"
  parser = OptionParser(usage)
  
  #options for the various parser

  # workflows.add_option("-c", "--Centralized-Workflow", dest="repository",
  #                   default=None, action = "append",
  #                   help="Checks the specified repository with the centralized workflow checker")

  parser.add_option("-f", "--Feature-Branch-Workflow", dest="feature_branch_workflow",
                default=None, action = "store", type="string",
                help="Checks the specified repository with the feature branch workflow checker", metavar="repository")

  parser.add_option("-e", "--Director-Lieutenant-Workflow", dest="director_lieutenant_workflow",
                default=None, action = "store", type="string",
                help="Checks the specified repository with the director lieutenant workflow checker")

  # parser.add_option("-g", "--Gitflow-Workflow", dest="gitflow-_workflow",
  #               default=None, action = "store", type="string",
  #               help="Checks the specified repository with the Gitflow workflow checker", metavar="repository")

  # parser.add_option("-j", "--Forking-Workflow", dest="forking_workflow",
  #               default=None, action = "store", type="string",
  #               help="Checks the specified repository with the forking workflow checker", metavar="repository")
  
  # parser.add_option("-s", "--Subversion-Workflow", dest="subversion_workflow",
  #               default=None, action = "store", type="string",
  #               help="Checks the specified repository with the subversion workflow checker", metavar="repository")
  
  # parser.add_option("-d", "--Distributed-Workflow", dest="distributed_workflow",
  #               default=None, action = "store", type="string",
  #               help="Checks the specified repository with the distributed workflow checker", metavar="repository")
  

  
  (options, args) = parser.parse_args()

  # Count the number of args to test for mutual exclusion.
  count = 0
  if (options.feature_branch_workflow):
    count = count + 1
  if (options.director_lieutenant_workflow):
    count = count + 1

  #will change later to make feature branch the default workflow!! when no options are given!!!!
  if count == 0:
    print args[0]
    clonecheck(None, args[0])
    sys.exit(1)
  elif count > 1:
    parser.error("Options are mutually exclusive!")

  #pasrse dictionary, clone repos, create meta data, and do check
  for key, value in options.__dict__.items():
      if value == None:
        continue
      clonecheck(key, value)
      sys.exit(1)


  # If there is a readme file, show it to the user. 
  try:
    readme_file = open('README.txt', 'r')
    for line in readme_file.readlines():
      print line
    readme_file.close()
  except IOError:
    # There is no readme file, or we can't access it.
    pass




def clonecheck(key, value):



    # If we end up here, the line contains a Git URL for us to clone
    print "Checking out repo from", value, "..."
    git_process = subprocess.Popen("git clone " + value, cwd = os.getcwd(), shell = True, 
       stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    (stdout_data, stderr_data) = git_process.communicate()

    os.chdir("./" + value.split('/')[-1])

    #create metadata
    #parse commits go here!!!

    parse_repository.parse_driver()


    #check
    #option to call module goes here
    # if(key == feature_branch_workflow):

    # if(key == director_lieutenant_workflow):

      

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

if __name__ == "__main__":
    main(sys.argv)