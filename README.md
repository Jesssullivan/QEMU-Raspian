# clipi:


***An efficient toolset for Pi devices***

*Emulate, organize, burn, manage a variety of distributions for Raspberry Pi.*


`clipi` offers an interactive command line application designed to streamline the deployment of Raspberry Pi devices.  `clipi` is written in Python for Debian-based operating systems, with experimental support for Mac OS via [brew](https://brew.sh/).
<br>        
- - -

### Choose your own adventure....


***Emulate:***    
`clipi` virtualizes many common sbc operating systems with QEMU.  Select from any of the included distributions (or add your own to [/sources.py](https://github.com/Jesssullivan/clipi/blob/master/sources.py)!) and `clipi` will handle the rest. xD

***Organize:***    
`clipi` builds and maintains organized directories for each OS as well as a persistent QEMU disk image.  Too many huge *.iso* files?  `clipi` cleans up after itself too under the ```Utilities...``` menu.

***Write:***    
`clipi` burns bootable disks too.  Just insert a sd card or disk and follow the friendly prompts.  
- *Need to pre-configure wifi?  Add your ssid and password to [/wpa_supplicant.conf](https://github.com/Jesssullivan/clipi/blob/master/wpa_supplicant.conf) and copy the file to `/boot` in the freshly burned disk.*    

- *Need pre-enabled ssh? copy [/ssh](https://github.com/Jesssullivan/clipi/blob/master/ssh) to `/boot` too.*

***Manage:***   
`clipi` can find the addresses of all the  Raspberry Pi devices on your local network.   Need to do this a lot?  `clipi` can install itself as a Bash alias, fire it up whenever you want xD
    
***Shortcuts:***             
Shortcuts & configuration arguments can be passed to `clipi` as a [.toml](https://github.com/toml-lang/toml) file.              
- Supply a shortcut file like so:          
```python3 clipi.py etc/qemu_stretchlite.toml```         
- Check out some other examples in [/etc](https://github.com/Jesssullivan/clipi/tree/master/etc).


- - -

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

- - -

