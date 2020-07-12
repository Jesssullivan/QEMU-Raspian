"""
# TODO: implement these network bridge methods
# (...or come up with a better guest to guest bridging system lol)
@classmethod
def get_network_depends(cls):
    if platform == 'darwin':
        print('cannot install network bridge depends on mac OSX')
        return 0
    else:
        print('make sure /network is ready to install....')
        subprocess.Popen('sudo chmod u+x network/apt_depends.sh', shell=True).wait()
        print('installing.....')
        subprocess.Popen('./network/apt_depends.sh', shell=True).wait()
        sleep(.1)
        print('done.')


@classmethod
def start_dhclient(cls):
    if platform == 'darwin':
        print('cannot use dhclient networking on mac OSX')
        return 0
    else:
        print('launching dhclient thread.....')
        subprocess.Popen('sudo chmod u+x network/dhclient.sh', shell=True).wait()
        sleep(.25)
        subprocess.Popen('./network/dhclient.sh', shell=True).wait()
        sleep(.1)
        print('exited dhclient thread.')
        sleep(.1)
"""
