@classmethod
def build_arm64(self, image=''):
    if not os.path.exists(names.src_dir(image)):
        os.mkdir(names.src_dir(image))
    if not os.path.exists(names.src_build(image)):
        os.mkdir(names.src_build(image))
    if not os.path.exists(names.src_mnt(image)):
        os.mkdir(names.src_mnt(image))
    image = 'img.img'

    # just continues with the last file / partition
    for disk in fdisk.read(image).keys():
        offset = fdisk.read(image)[disk]['Start']

    mount_cmd = str("sudo losetup -o " +
                    str(offset) +
                    ' /dev/loop12 ' +
                    image)

    mnt = subprocess.Popen(mount_cmd,
                           shell=True)

    for f in os.listdir(names.src_mnt(image)):
        print(f)
        if 'vmlinuz' in f:
            cp_cmd = 'cp ' + str(f) + names.src_build(image)

    mount_vm = str("sudo mount -v -o offset=" +
                   str(offset * 512) +
                   " -t ext4 " +
                   image + ' ' +
                   names.src_mnt(image))