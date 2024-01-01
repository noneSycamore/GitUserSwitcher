import ctypes
import sys
import GlobalValue

git_config_file_path = GlobalValue.getGitConfigFilePath()

def RequestHighPrivilege(gitConfig):
    """
    请求管理员权限 - (unused)
    """
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():  # if is already in administrator mode
            # do something
            with open(git_config_file_path, 'w') as configfile:
                gitConfig.write(configfile)
        else:  # if not, request administrator privilege, and restart this script
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)
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
        print(f'Unable to set attribute <{FILE_ATTRIBUTE}> for file \"{filepath}\".\nPlease add it manually.')
        sys.exit(0)

# 移除文件属性
def remove_attribute(filepath, FILE_ATTRIBUTE):
    ret = ctypes.windll.kernel32.SetFileAttributesW(filepath, get_file_attributes(filepath) & ~FILE_ATTRIBUTE)
    if not ret:
        print(f'Unable to remove attribute <{FILE_ATTRIBUTE}> for file \"{filepath}\".\nPlease remove it manually.')
        sys.exit(0)

# 检测并移除影响文件改动的文件属性
def detect_and_remove_attribute():
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

# 添加最开始移除的文件属性
def add_removed_attribute(removed_attributes):
    for attribute in removed_attributes:
        add_attribute(git_config_file_path, attribute)
