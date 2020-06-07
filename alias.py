#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""
from sys import platform
from common import *

"""
alias.py:
copy / update files at ~/.clipi to be accessed via alias.
add clipi to shell's rc file.  
"""


def add_to_bash():
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


def bash_alias_update():
    # adds .directory for bash version, separate from git:
    if not os.path.exists('~/.clipi'):
        subprocess.Popen("mkdir ~/.clipi", shell=True).wait()

    if not os.path.exists('~/.clipi/bin/'):
        subprocess.Popen("mkdir ~/.clipi/bin/", shell=True).wait()

    print('copying *.py to ~/.clipi/*....')
    subprocess.Popen('sudo cp -rf ' + os.path.relpath('*.py') +
                     ' ~/.clipi/*', shell=True).wait()

    print('copying bin to ~/.clipi/bin/....')
    subprocess.Popen('sudo cp -rf ' + os.path.relpath('bin') +
                     ' ~/.clipi/bin/', shell=True).wait()

    # this is very unlikely to still be needed-
    subprocess.Popen('sudo chmod 775 ~/.clipi/clipi.py', shell=True).wait()
