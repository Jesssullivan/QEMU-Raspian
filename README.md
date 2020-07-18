# clipi:


***An efficient toolset for Pi devices***

*Emulate, organize, burn, manage a variety of distributions for Raspberry Pi.*

- - -

### Choose your own adventure....


***Emulate:***    
`clipi` virtualizes many common sbc operating systems with QEMU, and can play with both 32 bit and 64 bit operating systems.    
-  *Select from any of the included distributions (or add your own to [/sources.toml](https://github.com/Jesssullivan/clipi/blob/master/etc/sources.toml)!) and `clipi` will handle the rest.*
        
***Organize:***    
`clipi` builds and maintains organized directories for each OS as well a [persistent & convenient .qcow2](https://www.qemu.org/docs/master/interop/qemu-img.html)  QEMU disk image.           
-   Too many huge source *.img* files and archives?  `clipi` cleans up after itself under the ```Utilities...``` menu.      
-   additional organizational & gcc compilation methods are available in [/kernel.py](https://github.com/Jesssullivan/clipi/tree/master/kernel.py) 
    
***Write:***    
`clipi` burns emulations to external disks!  Just insert a sd card or disk and follow the friendly prompts.  All files, `/home`, guest directories are written out.
- *Need to pre-configure (or double check) wifi?  Add your ssid and password to [/wpa_supplicant.conf](https://github.com/Jesssullivan/clipi/blob/master/wpa_supplicant.conf) and copy the file to `/boot` in the freshly burned disk.*     
- *Need pre-enabled ssh? copy [/ssh](https://github.com/Jesssullivan/clipi/blob/master/ssh) to `/boot` too.*            
- *`clipi` provides options for writing from an emulation's `.qcow2` file via qemu...*         
- *...as well as from the [source's](https://github.com/Jesssullivan/clipi/blob/master/etc/sources.toml) raw image file with the `verbatim` argument*           
    
        
***Manage:***   
`clipi` can find the addresses of all the Raspberry Pi devices on your local network.       
- *Need to do this a lot?  `clipi` can install itself as a Bash alias (option under the ```Utilities...``` menu, fire it up whenever you want.*          

    
***Shortcuts:***      
       
Shortcuts & configuration arguments can be passed to `clipi` as a [.toml](https://github.com/toml-lang/toml) ([or yaml](https://yaml.org/)) file.              
-  *Shortcut files access clipi's tools in a similar fashion to the interactive menu:*       
   
```toml
# <shortcut>.toml
# you can access the same tools and functions visible in the interactive menu like so:
'Burn a bootable disk image' = true  
# same as selecting in the interactive cli
'image' = 'octoprint'
'target_disk' = 'sdc'  
```     
-  *`clipi` exposes many features only accessible via configuration file arguments, such as distribution options and emulation settings.*

```toml
# <shortcut>.toml
# important qemu arguments can be provided via a shortcut file like so:
'kernel' = "bin/ddebian/vmlinuz-4.19.0-9-arm64"
'initrd' = "bin/ddebian/initrd.img-4.19.0-9-arm64"
# qemu arguments like these use familiar qemu lexicon:
'M' = "virt" 
'm' = "2048"
# default values are be edited the same way:
'cpu' = "cortex-a53"
'qcow_size' = "+8G"
'append' = '"rw root=/dev/vda2 console=ttyAMA0 rootwait fsck.repair=yes memtest=1"'
# extra arguments can be passed too:
'**args' = " -device virtio-blk-device,drive=hd-root \\
             -netdev user,id=net0 -no-reboot \\
             -monitor stdio \\
             -device virtio-net-device,netdev=net0 "

```
    
-  *Supply a shortcut file like so:*           
```python3 clipi.py etc/find_pi.toml```   

- *take a look in [/etc](https://github.com/Jesssullivan/clipi/tree/master/etc) for some shortcut examples and default values*
         
        
- - - 
        
#### *TODOs & WIPs:*  

     
*bridge networking things:*        
-  working on guest --> guest, host --> bridge, host only mode networking options.
  as of 7/17/20 only SLiRP user mode networking works,
   see branch [broken_bridge-networking](https://github.com/Jesssullivan/clipi/tree/broken_bridge-networking) 
   to see what is currently cooking here 
   
         
*kernel stuff:*   
-  automate ramdisk & kernel extraction-
 most functions to do so are all ready to go in /kernel.py

- *other random kernel todos-*      
    -  working on better options for building via qemu-debootstrap from chroot instead of debian netboot or native gcc  
    -  add git specific methods to sources.py for mainline Pi linux kernel  
        -  verify absolute binutils version    
        -  need to get cracking on documentation for all this stuff       
        
    
*gcp-io stuff:*   
-  formalize ddns.py & dockerfile    
-  make sure all ports (22, 80, 8765, etc) can up/down as reverse proxy     

- - - 
    
<br>   
    
```shell script
# clone:
git clone https://github.com/Jesssullivan/clipi
cd clipi

# preheat:
pip3 install -r requirements.txt
# (or pip install -r requirements.txt)

# begin cooking some Pi:
python3 clipi.py
```         