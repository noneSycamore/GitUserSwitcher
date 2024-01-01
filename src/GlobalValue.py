import os
from CustomUtils import getOsName

# git config file
git_config_file_path_windows = os.path.expanduser('~\\.gitconfig')
git_config_file_path_linux = os.path.expanduser('~/.gitconfig')
OS = getOsName()

# prefix string in .gitconfig
prefixString = 'git-switcher \"'

def getGitConfigFilePath():
    if OS == 'Windows':
        return git_config_file_path_windows
    elif OS == 'Linux':
        return git_config_file_path_linux

def setGitConfigFilePath(path):
    global git_config_file_path_windows, git_config_file_path_linux
    if OS == 'Windows':
        git_config_file_path_windows = path
    elif OS == 'Linux':
        git_config_file_path_linux = path

def getPrefixString():
    return prefixString

def getOs():
    return OS