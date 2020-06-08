#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *

"""
alias.py:
copy / update files at ~/.clipi to be accessed via alias.
add clipi to shell's rc file.
"""


class alias(object):

    @classmethod
    def add_to_bash(cls):
        print('adding alias....')
        clipi_line = "\\'~/.clipi/clipi.py\\'"

        if platform == "linux" or platform == "linux2":
            print("environment: detected Linux, continuing...")
            cmd = "echo alias clipi=" + clipi_line + " >> ~/.bashrc "
            subprocess.Popen(cmd, shell=True).wait()

        if platform == 'darwin':
            print("environment: detected Mac OSX, continuing...")
            if os.path.exists('~/zshrc'):
                cmd = "echo alias clipi=" + clipi_line + " >> ~/.zshrc "
                subprocess.Popen(cmd, shell=True).wait()
            if os.path.exists('~/bashrc'):
                cmd = "echo alias clipi=" + clipi_line + " >> ~/.bashrc "
                subprocess.Popen(cmd, shell=True).wait()
            if os.path.exists('~/bash_profile'):
                cmd = "echo alias clipi=" + clipi_line + " >> ~/.bash_profile "
                subprocess.Popen(cmd, shell=True).wait()

    @classmethod
    def bash_alias_update(cls):
        # adds .directory for bash version, separate from git:
        try:
            subprocess.Popen("sudo rm -rf ~/.clipi", shell=True).wait()
        except:
            pass
        try:
            subprocess.Popen("sudo mkdir  ~/.clipi", shell=True).wait()
        except:
            pass
        try:
            subprocess.Popen("sudo cp -rf  ../clipi/* ~/.clipi/", shell=True).wait()
        except:
            pass
        try:
            subprocess.Popen("rm -rf ~/.clipi/.git", shell=True).wait()
        except:
            pass
        try:
            subprocess.Popen("sudo chmod 775 ~/.clipi/*", shell=True).wait()
        except:
            pass

    @classmethod
    def do_alias(cls):
        cls.add_to_bash()
        cls.bash_alias_update()
