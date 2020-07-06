import os
import subprocess
import configuration as conf
from ConfigurationFolder import ConfigurationFolder

class InstallError(Exception):
    """ Group Intaller exceptions"""
    pass

class Installer:
    def __init__(self):
        self.launch()

    def launch(self):
        """
        Install the custom configuration from a remote requisitory.
        Install selectionned programs.
        """
        # Avoid installing config if already installed
        if os.path.exists(conf.REQUISITORY_LOCATION):
            err_msg = "{} already exists.".format(conf.REQUISITORY_LOCATION)
            raise InstallError(err_msg)

        # Clone current configuration
        url = conf.REQUISITORY_URL
        destination = conf.REQUISITORY_LOCATION
        clone_cmd = subprocess.run(["git", "clone", url, destination])
        # Control clone error
        if clone_cmd.returncode is not 0:
            err_msg = "git clone failed with status {}."
            raise InstallError(err_msg.format(clone_cmd.returncode))

        self.move_files()

    def move_files(self):
        local_conf = ConfigurationFolder(conf.CONFIGURATION_DIRECTORY)
        remote_conf = ConfigurationFolder(conf.REQUISITORY_LOCATION)

        file_to_save = remote_conf.retrieve_files()
        local_conf.save_files(remote_conf.retrieve_files(), remote_conf.directory)
