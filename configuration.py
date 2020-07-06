import os

# Specify your git requisitory used for synchronization.

REQUISITORY_URL = "https://github.com/AbcSxyZ/configuration.git"
REQUISITORY_LOCATION = os.path.join(os.getenv("HOME"), \
    ".configuration/")

# Configuration folder of your local machine.
# HOME can be used. Search are perfomed with
# globbing patter so you can just follow some files/folders.

CONFIGURATION_DIRECTORY = os.getenv("HOME")

# All files and folder to follow.
# You can use globbing for matching file or folder.

FILES = [
        ".vimrc",
        ".vim/local/",
        ".vim/bundle/Vundle.vim/autoload",
        ".vim/colors/",
        ".tmux.conf",
        ".zshrc",
        ".vimrc_plugins",
        "important",
        ]

SHELL = "zsh"

PROGRAMS = [
        "tmux",
        "curl",
        "wget",
	"vim",
        ]

INSTALL_SCRIPT = {
        "urls" : [
            "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
            ],
        "local" : [],
    }
