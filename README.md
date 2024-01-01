# git-user-switcher
(abbreviated as gus)

 A Command Tool to Manage Global Git User. 

## Usage

Using `gus -h` for help information.

| Options                          | Description                                                  |
| -------------------------------- | ------------------------------------------------------------ |
| -h, --help                       | show help message and exit                                   |
| -s [SAVE ...], --save [SAVE ...] | Save user name and email to your custom symbol (default using your username).<br/>Example: --save symbol name email<br/> &emsp;&emsp; &emsp;&emsp;--save name email |
| -l, --list                       | List all custom symbols.                                     |
| -r REMOVE, --remove REMOVE       | Remove custom symbols.<br/>Example: --remove symbol          |
| -e [EDIT ...], --edit [EDIT ...] | Edit custom symbols.<br/>Example: --edit symbol name email   |
| -c CHANGE, --change CHANGE       | Change git user.<br/>Example: change symbol                  |

## Other
Config info is stored directly in the `.gitconfig` file.
