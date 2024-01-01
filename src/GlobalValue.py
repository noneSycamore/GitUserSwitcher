import os

# git config file
git_config_file_path = os.path.expanduser('~\\.gitconfig')

# prefix string in .gitconfig
prefixString = 'git-switcher \"'

def getGitConfigFilePath():
    return git_config_file_path

def setGitConfigFilePath(path):
    global git_config_file_path
    git_config_file_path = path

def getPrefixString():
    return prefixString
