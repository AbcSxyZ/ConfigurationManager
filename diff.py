import subprocess
import os
import difflib
from colors import *

class DiffTool:
    """
    Perfom diff on two configuration.
    From each directory, can perfom diff on same filename,
    or check which file remain untracked.
    """
    def __init__(self, local_config, remote_config):
        self.local = local_config
        self.local_files = set(local_config.cleaned_files())
        self.remote = remote_config
        self.remote_files = set(remote_config.cleaned_files())

    def display_diff(self):
        """
        Get output of all diff and untracked files, and
        display them if existing.
        """
        files_diff = self.perform_diff()
        files_untrack = self.check_untracked()
        final_display = None
        if len(files_diff) > 0 and files_untrack is not None:
            final_display = files_diff + "\n" + files_untrack
        else:
            final_display = files_diff if len(files_diff) > 0 else files_untrack
        if final_display is not None:
            print(final_display)
            return 1
        return 0

    def perform_diff(self):
        """
        Retrieve all commons files between the configuration
        and perform a diff on their content.
        Return a formated string with the result of this diff.
        """
        common_files = self.local_files & self.remote_files
        performed_diff = 0
        diff_repr = ""
        for filename in common_files:
            # Open and retrieve the content of the file in both directory
            local_name = os.path.join(self.local.directory, filename)
            remote_name = os.path.join(self.remote.directory, filename)
            with open(local_name) as local_stream,\
                    open(remote_name) as remote_stream:
                local_content = local_stream.readlines()
                remote_content = remote_stream.readlines()

            # Perform the diff
            diff_res = difflib.unified_diff(local_content, remote_content,\
                    fromfile=local_name, tofile=remote_name)
            diff_res = list(diff_res)

            # Concat the output with other file diff
            if len(diff_res) > 0:
                display_filename = "{}{}{}\n\n".\
                        format(GREEN, filename, RESET)
                if performed_diff != 0:
                    display_filename = "\n" + display_filename
                else:
                    diff_repr += YELLOW + "Diff status : \n" + RESET
                performed_diff += 1
                diff_res = "".join([display_filename] + diff_res)
                diff_repr += diff_res
        return diff_repr

    def check_untracked(self):
        """
        Retrieve all files or directory which are only one the
        local or the remote directory.
        Check in which of this directories the element in contained.
        Return formatted string of untracked files by folder.
        """
        untracked_files = self.local_files ^ self.remote_files
        local_untracked = []
        remote_untracked = []
        for filename in untracked_files:
            if filename in self.local_files:
                local_untracked.append(filename)
            else:
                remote_untracked.append(filename)

        # For the remote and the local directory
        # format in a string all untracked files
        local_repr = None
        remote_repr = None
        path_color = lambda path : GREEN + "{}:\n".format(path) + RESET
        if len(local_untracked) > 0:
            local_repr =  path_color(self.local.directory)
            local_repr += "\n".join(local_untracked)
        if len(remote_untracked) > 0:
            remote_repr = path_color(self.remote.directory)
            remote_repr += "\n".join(remote_untracked)

        # Try to concatenate the local and remote untracked files
        # Otherwise, return only the folder with untracked files, or None.
        if local_repr is None and remote_repr is None:
            return None
        display_untrack = RED + "Untracked files : \n" + RESET
        if local_repr and remote_repr:
            return display_untrack + local_repr + "\n\n" + remote_repr
        if local_repr:
            return display_untrack + local_repr
        return display_untrack + remote_repr
