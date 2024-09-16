from setuptools import find_packages,setup
from typing import List

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."


# we want to read the "requirements.txt" file and get a
# list of strings of what all ibraries we will require for our  
# project because "requirements.txt" file contains all the 
# libraries and other stuffs needed for our project                                          
def get_requirements() -> List[str]:  # this tells that "this function returns a list of strings"
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()   # this will read line by line
    requirement_list = [requirement_name.replace("/n","") for requirement_name in requirement_list]
    # this will replace "/n" with "nothing" -- because "/n" is extra in each line
    # also there is one "-e ." which is not a library -- so we have to not include it in our
    # list of strings
    if HYPHEN_E_DOT in requirement_list :
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

                                
setup(
    name = "sensor",
    version = "0.0.1",
    author = "Sumanth",
    author_email = "sumanthhegde321@gmail.com",
    packages = find_packages(),    # thia is used so that all the source codes it will find and 
                                   # consider it as a part of this same project
                                   # any folder which contains the "__init__.py" file -- it will be 
                                   # considered as a part of this project or package
                                   # and "find_packages()" will search for all these and consider
                                   # them to be a part of this project or package
                                   # As of now, only the "sensor" folder contains "__init__.py" 
                                   # so, as of now,  only this folder is considered to be a part of 
                                   # project and only this folder's info too is present 
                                   # in "setup.egg-info"
                                   
                                               
    install_requires = get_requirements(),   # "get_requirements()" will give us a list of what all 
                                             # libraries we will require in our project
)

