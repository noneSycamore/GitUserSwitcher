import ctypes
import sys
import os
import stat

import GlobalValue
from CustomUtils import changeColor

git_config_file_path = GlobalValue.getGitConfigFilePath()
OS = GlobalValue.getOs()

def RequestHighPrivilege(gitConfig):
    """
    请求管理员权限 - (unused)
    """
    try:
        if OS == 'Windows':  # request administrator privilege if on Windows
            if ctypes.windll.shell32.IsUserAnAdmin():  # if is already in administrator mode
                with open(git_config_file_path, 'w') as configfile:
                    gitConfig.write(configfile)
            else:  # if not, request administrator privilege, and restart this script
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)
        elif OS == 'Linux':  # tell user to run as root if on Linux
            if os.geteuid() != 0:  # if not root
                print(changeColor('Please run this script as root.', 'red'))
                sys.exit(0)
            else:
                with open(git_config_file_path, 'w') as configfile:
                    gitConfig.write(configfile)
    except Exception as e:
        print('Please run this script as administrator.')
        sys.exit(0)

# 获取文件属性
def get_file_attributes(filepath):
    return ctypes.windll.kernel32.GetFileAttributesW(filepath)

# 设置文件属性
def add_attribute(filepath, FILE_ATTRIBUTE):
    ret = ctypes.windll.kernel32.SetFileAttributesW(filepath, get_file_attributes(filepath) | FILE_ATTRIBUTE)
    if not ret:
        print(f'Failed to set attribute <{FILE_ATTRIBUTE}> for file \"{filepath}\".\nPlease add it manually.')
        sys.exit(0)

# 移除文件属性
def remove_attribute(filepath, FILE_ATTRIBUTE):
    ret = ctypes.windll.kernel32.SetFileAttributesW(filepath, get_file_attributes(filepath) & ~FILE_ATTRIBUTE)
    if not ret:
        print(f'Failed to remove attribute <{FILE_ATTRIBUTE}> for file \"{filepath}\".\nPlease remove it manually.')
        sys.exit(0)

# 检测并移除影响文件改动的文件属性
def detect_and_remove_attribute():
    if OS == 'Windows':
        original_attributes = get_file_attributes(git_config_file_path)
        removed_attributes = []
        # if file is read-only, remove read-only attribute
        if original_attributes & 0x01:
            remove_attribute(git_config_file_path, 0x01)
            removed_attributes.append(0x01)
        
        # if file is hidden, remove hidden attribute
        if original_attributes & 0x02:
            remove_attribute(git_config_file_path, 0x02)
            removed_attributes.append(0x02)
        return removed_attributes
    elif OS == 'Linux':
        if not os.access(git_config_file_path, os.W_OK):
            try:
                os.chmod(git_config_file_path, stat.S_IWUSR)
                return ['read']
            except Exception as e:
                print(f'Failed to change the permission of \"{git_config_file_path}\" to write.\nPlease change the permission manually.')
                sys.exit(0)
        else:
            return []

# 添加最开始移除的文件属性
def add_removed_attribute(removed_attributes):
    if OS == 'Windows':
        for attribute in removed_attributes:
            add_attribute(git_config_file_path, attribute)
    elif OS == 'Linux':
        if 'read' in removed_attributes:
            try:
                os.chmod(git_config_file_path, stat.S_IRUSR)
            except Exception as e:
                print(f'Failed to change the permission of \"{git_config_file_path}\" back to read.\nPlease change the permission back manually.')
                sys.exit(0)
