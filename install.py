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
        self.install_programs()
        self.run_scripts()
        # self.configure_shell()

    def move_files(self):
        """
        When the remote repository is cloned, transfer file
        to the compture local CONFIGURATION_DIRECTORY.
        """
        local_conf = ConfigurationFolder(conf.CONFIGURATION_DIRECTORY)
        remote_conf = ConfigurationFolder(conf.REQUISITORY_LOCATION)

        file_to_save = remote_conf.retrieve_files()
        local_conf.save_files(remote_conf.retrieve_files(), remote_conf.directory)

    # def configure_shell(self):
    #     """
    #     Setup SHELL indicated in configuration as the default shell.
    #     """
    #     shell_path = subprocess.check_output(['which', conf.SHELL]).decode()
    #     subprocess.run(["chsh", "--shell", shell_path])

    def install_programs(self):
        """
        Install list of default programs indicated by PROGRAMS config.
        """
        list_programs = [conf.SHELL] + conf.PROGRAMS

        for program in list_programs:
            check_exists = subprocess.run(["which", program],
                    stdout=subprocess.DEVNULL)
            if check_exists.returncode != 0:
                subprocess.run(["sudo", "apt", "install", "-y", program])

    def run_scripts(self):
        for script_filename in conf.INSTALL_SCRIPT['urls']:
            script = self.get_raw_script(script_filename, curl=True)
            subprocess.run([conf.SHELL, "-c", script]) 

        for script_filename in conf.INSTALL_SCRIPT['local']:
            script = self.get_raw_script(script_filemane)
            subprocess.run([conf.SHELL, "-c", script]) 

    @staticmethod
    def get_raw_script(filename, curl=False):
        """
        Retrieve an installation shell script, remotely or localy.
        Return content of the shell script.
        """
        if curl:
            return subprocess.check_output(["curl", filename]).decode()

        with open(filename, "r") as script_file:
            content = script_file.read()
        return content
