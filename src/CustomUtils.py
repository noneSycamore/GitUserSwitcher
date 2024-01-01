import platform

def changeColor(text, color):
    """
    change 'help' text color using ANSI escape code
    """
    if color == 'red':
        return '\033[1;31m' + text + '\033[0m'
    elif color == 'green':
        return '\033[1;32m' + text + '\033[0m'
    elif color == 'yellow':
        return '\033[1;33m' + text + '\033[0m'
    elif color == 'blue':
        return '\033[1;34m' + text + '\033[0m'
    elif color == 'purple':
        return '\033[1;35m' + text + '\033[0m'
    elif color == 'cyan':
        return '\033[1;36m' + text + '\033[0m'
    elif color == 'white':
        return '\033[1;37m' + text + '\033[0m'
    else:
        return text

def getOsName():
    """
    return OS name
    """
    if platform.system() == 'Windows':
        return 'Windows'
    elif platform.system() == 'Linux':
        return 'Linux'
    elif platform.system() == 'Darwin':
        return 'Mac'
    else:
        return 'Unknown'