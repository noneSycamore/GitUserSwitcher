import configparser
import argparse

import GlobalValue
import FileAttributeManage
from CustomUtils import changeColor
import CheckArguments

git_config_file_path = GlobalValue.getGitConfigFilePath()
prefixString = GlobalValue.getPrefixString()


def init_parser():
    """
    配置argparse
    """
    # argparse for command line
    parser = argparse.ArgumentParser(description="A Command Tool to Change Global Git Config.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--save', nargs='*', action=CheckArguments.CheckSave, type=str,
                       help='Save user name and email to your custom symbol (default using your username).\n' +
                            changeColor('Example: ', 'yellow') + changeColor('--save symbol name email', 'green') +
                            '\n         ' + changeColor('--save name email', 'green'))
    group.add_argument('-l', '--list', action='store_true',
                       help='List all custom symbols.\n')
    group.add_argument('-r', '--remove', type=str,
                       help='Remove custom symbols.\n' +
                            changeColor('Example: ', 'yellow') + changeColor('--remove symbol', 'green'))
    group.add_argument('-e', '--edit', nargs='*', action=CheckArguments.CheckEdit, type=str,
                       help='Edit custom symbols.\n' +
                            changeColor('Example: ', 'yellow') + changeColor('--edit symbol name email', 'green'))
    group.add_argument('-c', '--change', type=str,
                       help='Change git user.\n' +
                            changeColor('Example: ', 'yellow') + changeColor('change symbol', 'green'))
    args = parser.parse_args()

    if args.list:
        print()
        PrintCustomSymbols()
    if args.save:
        print()
        SaveCustomSymbols(args.save)
    if args.remove:
        print()
        RemoveCustomSymbols(args.remove)
    if args.edit:
        print()
        EditCustomSymbols(args.edit)
    if args.change:
        print()
        ChangeGitConfig(args.change)


def SaveCustomSymbols(dataList):
    """
    Save custom symbols (if not exist).

    Parameters:
    dataList (list): A list containing symbol, name, and email (in that order) or name and email.
    """
    gitConfig = configparser.ConfigParser()
    gitConfig.read(git_config_file_path)

    symbolData = dataList[0]
    if len(dataList) == 2:
        nameData = dataList[0]
        emailData = dataList[1]
    elif len(dataList) == 3:
        nameData = dataList[1]
        emailData = dataList[2]

    # check if symbol is already exist
    for section in gitConfig.sections():
        if section.startswith(prefixString):
            if gitConfig.get(section, 'symbol') == symbolData:
                print(changeColor("Symbol is Already Exist!", 'red'))
                return
    sectionName = prefixString + symbolData + '\"'
    gitConfig.add_section(sectionName)
    gitConfig.set(sectionName, 'symbol', symbolData)
    gitConfig.set(sectionName, 'name', nameData)
    gitConfig.set(sectionName, 'email', emailData)

    with open(git_config_file_path, 'w') as configfile:
        gitConfig.write(configfile)
    print(changeColor('Save Success.', 'green'))


def PrintCustomSymbols():
    """
    print all custom symbols
    """
    gitConfig = configparser.ConfigParser()
    gitConfig.read(git_config_file_path)

    # print current user
    currentUserName = ''
    currentUserEmail = ''
    currentSymbol = ''
    for section in gitConfig.sections():
        if section == 'user':
            currentUserName = gitConfig.get(section, 'name')
            currentUserEmail = gitConfig.get(section, 'email')
            break
    if currentUserName != '' and currentUserEmail != '':
        flag = False
        for section in gitConfig.sections():
            if section.startswith(prefixString):
                if gitConfig.get(section, 'name') == currentUserName and gitConfig.get(section,
                                                                                       'email') == currentUserEmail:
                    currentSymbol = gitConfig.get(section, 'symbol')
                    flag = True
                    break
        if flag:
            print(changeColor('Current User: \n    ', 'yellow') + changeColor(currentSymbol,
                                                                              'green') + ': ' + currentUserName + ' <' + changeColor(
                currentUserEmail, 'blue') + '>')
        else:
            print(changeColor('Current User: ', 'yellow'))
            print('    ' + currentUserName + ' <' + changeColor(currentUserEmail, 'blue') + '>' + changeColor(
                '\n    (Current User Info is Not Saved as Custom Symbols.)', 'red'))
    else:
        print(changeColor('No Current User.', 'red'))

    # print custom symbols
    print('\n' + changeColor('Custom Symbols:', 'yellow'))
    flag = False
    for section in gitConfig.sections():
        if section.startswith(prefixString):
            print('    ' + changeColor(gitConfig.get(section, 'symbol'), 'green') + ': ' + gitConfig.get(section,
                                                                                                         'name') + ' <' + changeColor(
                gitConfig.get(section, 'email'), 'blue') + '>')
            flag = True
    if not flag:
        print(changeColor('\nNo Custom Symbols.', 'yellow'))
    else:
        print(changeColor('\nPrint Success.', 'green'))


def RemoveCustomSymbols(symbol):
    """
    remove custom symbols (if exist)
    """
    gitConfig = configparser.ConfigParser()
    gitConfig.read(git_config_file_path)

    flag = False
    for section in gitConfig.sections():
        if section.startswith(prefixString):
            if gitConfig.get(section, 'symbol') == symbol:
                gitConfig.remove_section(section)
                flag = True
                break
    if not flag:
        print(changeColor('No Such Symbol.', 'red'))
    else:
        with open(git_config_file_path, 'w') as configfile:
            gitConfig.write(configfile)
        print(changeColor('Remove Success.', 'green'))


def EditCustomSymbols(dataList):
    """
    edit custom symbols (if exist)
    """
    gitConfig = configparser.ConfigParser()
    gitConfig.read(git_config_file_path)

    symbolData = dataList[0]
    nameData = dataList[1]
    emailData = dataList[2]

    flag = False
    # check if symbol is already exist
    for section in gitConfig.sections():
        if section.startswith(prefixString):
            if gitConfig.get(section, 'symbol') == symbolData:
                flag = True
                break
    if not flag:
        print(changeColor('No Such Symbol.', 'red'))
        return
    sectionName = prefixString + symbolData + '\"'
    gitConfig.set(sectionName, 'symbol', symbolData)
    gitConfig.set(sectionName, 'name', nameData)
    gitConfig.set(sectionName, 'email', emailData)

    with open(git_config_file_path, 'w') as configfile:
        gitConfig.write(configfile)
    print(changeColor('Save Success.', 'green'))


def ChangeGitConfig(symbol):
    """
    switch git user to symbol
    """
    gitConfig = configparser.ConfigParser()
    gitConfig.read(git_config_file_path)

    nameData = ''
    emailData = ''
    currentUserName = ''
    currentUserEmail = ''
    for section in gitConfig.sections():
        if section.startswith(prefixString):
            if gitConfig.get(section, 'symbol') == symbol:
                nameData = gitConfig.get(section, 'name')
                emailData = gitConfig.get(section, 'email')
        if section == 'user':
            currentUserName = gitConfig.get(section, 'name')
            currentUserEmail = gitConfig.get(section, 'email')

    # check if symbol is already exist
    if nameData == currentUserName and emailData == currentUserEmail:
        print(changeColor('Already Using This User.', 'yellow'))
        return

    # change user
    if nameData != '' and emailData != '':
        gitConfig.set('user', 'name', nameData)
        gitConfig.set('user', 'email', emailData)
        with open(git_config_file_path, 'w') as configfile:
            gitConfig.write(configfile)
        print(changeColor('Change Success.', 'green'))
    else:
        print(changeColor('No Such Symbol or Something Wrong With This Symble, Please Check It.', 'red'))


if __name__ == '__main__':
    removed_attributes = FileAttributeManage.detect_and_remove_attribute()
    init_parser()
    FileAttributeManage.add_removed_attribute(removed_attributes)
