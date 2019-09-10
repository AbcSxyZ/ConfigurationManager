import os

# Specify your git requisitory used for synchronization.

REQUISITORY_LOCATION = os.path.join(os.getenv("HOME"), \
    "Documents/configuration/")

# Configuration folder of your local machine.
# HOME can be used. Search are perfomed with
# globbing patter so you can just follow some files/folders.

CONFIGURATION_DIRECTORY = os.getenv("HOME")

# All file and folder to follow.
# You can use globbing for matching file or folder.

FILES = [
        ".vimrc",
        ".vim/local/",
        ".tmux.conf",
        ".zshrc",
        ".vimrc_plugins",
        "important",
        ]
