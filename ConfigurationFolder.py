from distutils import dir_util
import os
import glob
import configuration as conf
import subprocess
import datetime
from colors import *

def pull_wrap(function):
    """
    Try to pull the content of the remote requisitory
    before the function's calling.
    """
    def wrapper(self, *args, **kwargs):
        self.pull()
        return function(self, *args, **kwargs)
    return wrapper

def cd_config(function):
    """
    Decorate ConfigurationFolder function to
    move in the directory of the configuration.
    """
    def directory_wrap(self, *args, **kwargs):
        with self:
            return function(self, *args, **kwargs)
    return directory_wrap

def git_log(function):
    """
    Delimitate git logs with colors.
    """
    def git_wrapper(self, *args, **kwargs):
        if self.git == False:
            return function(self, *args, **kwargs)
        print(YELLOW + "--------- Git Log ---------\n" + RESET)
        status = function(self, *args, **kwargs)
        print(YELLOW + "\n---------------------------" + RESET)
        return status
    return git_wrapper


class ConfigurationFolder:
    """
    Manipulate a configuration folder.
    Retrieve, create or delete files inside the folder.
    Perform push and pull request on git requisitory.
    """
    def __init__(self, directory):
        self.directory = directory
        with self:
            self.git = os.path.isdir(os.path.join(self.directory, ".git"))

    @pull_wrap
    def retrieve_files(self, pattern=None):
        """
        For the given directory, retrieve all matching files according
        to the configuration. All file who will be saved or
        loaded depending of the user action.
        Retrieve only files, perform recursive search on directories.
        """
        expected_files = []
        for filepattern in conf.FILES:
            filepattern = os.path.join(self.directory, filepattern)

            # Recursive file search for a directory
            if os.path.isdir(filepattern):
                expected_files.extend(self.folder_parse(filepattern))

            # Retrieve globbing match and perform recursive search
            # on directory or append the regular file.
            else:
                for path in glob.glob(filepattern):
                    if os.path.isdir(path):
                        expected_files.extend(self.folder_parse(path))
                    elif os.path.isfile(path):
                        expected_files.append(path)
        return expected_files

    def folder_parse(self, foldername):
        """
        List all filename containing in the given foldername.
        Search recursively all files.
        """
        dirfiles = os.listdir(foldername)
        list_files = []
        for filename in dirfiles:
            filename = os.path.join(foldername, filename)
            if os.path.isdir(filename):
                list_files.extend(self.folder_parse(filename))
            elif os.path.isfile(filename):
                list_files.append(filename)
        return list_files


    def cleaned_files(self):
        """
        Retrieve all configuration files and folder, but remove
        the directory name from the path.
        Get relative directory from the configuration directory.
        """
        config_files = self.retrieve_files()
        len_dirname = len(self.directory)
        clean_files = []
        for filename in config_files:
            clean_name = filename.replace(self.directory, "")
            if clean_name[0] == "/":
                clean_name = clean_name[1:]
            clean_files.append(clean_name)
        return clean_files

    @cd_config
    def remove_files(self, pattern_list):
        """
        Remove files according to a list of globbing pattern.
        Remove regular and directory files.
        """
        modified_files = []
        for pattern in pattern_list:
            for pathname in glob.glob(pattern):
                if os.path.isdir(pathname):
                    dir_util.remove_tree(pathname)
                elif os.path.isfile(pathname):
                    os.unlink(pathname)
                modified_files.append(pathname)
                if pattern in conf.FILES:
                    msg = "{} : remove {} from the configuration" + \
                    " to avoid the tracking."
                    print(msg.format(sys.argv[0], pattern))
        self.push(modified_files, "delete")

    def check_folder(self, filename):
        """
        Verify if the folder containing the file is already existing.
        Create it otherwise.
        """
        expected_dir = os.path.dirname(filename)
        if len(expected_dir) > 0 and os.path.exists(expected_dir) == False:
            os.makedirs(expected_dir)

    @cd_config
    def save_files(self, files, parent_directory):
        """
        Copy the given list of files which are comming from parent_directory
        to the ConfigurationFolder directory.
        Preserve the file and folder architecture.
        """
        session_files = []
        for save_file in files:
            #Remove the parent_directory folder from the filename 
            #to convert this file in an absolute filename for the
            #configuration directory.
            default_path = save_file.replace(parent_directory, "")
            if default_path[0] == "/":
                default_path = default_path[1:]
            self.check_folder(default_path)
            local_location = os.path.join(self.directory, default_path)
            if os.path.isfile(save_file):
                with open(save_file, "r") as src, open(local_location, "w") as dst:
                    res = dst.write(src.read())
            elif os.path.isdir(save_file):
                dir_util.copy_tree(save_file, local_location)
            session_files.append(local_location)
        self.push(session_files, "save")

    @git_log
    def push(self, added_files, action):
        """
        If a configuration folder is a git requisitory,
        push current modifications.
        Can add/modify or delete files.
        """
        if self.git:
            date = str(datetime.datetime.now())
            date = date.split('.')[0]
            commit_msg = "Update : {} configuration files - {}.".\
                    format(action.capitalize(), date)
            subprocess.run(["git", "add"] + added_files)
            subprocess.run(["git", "commit", "-m", commit_msg])
            subprocess.run(["git", "push"])

    @git_log
    def pull(self):
        """
        Pull request on git requisitory.
        """
        if self.git:
            with self:
                subprocess.run(["git", "pull"])


    def __enter__(self):
        self._save_dir = os.getcwd()
        os.chdir(self.directory)
        return self

    def __exit__(self, *args):
        os.chdir(self._save_dir)

    def __str__(self):
        conf_str = "<Configuration {}".format(self.directory)
        if self.git:
            conf_str += " - Git"
        conf_str += ">"
        return conf_str


