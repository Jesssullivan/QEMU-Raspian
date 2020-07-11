# clipi:


***An efficient toolset for Pi devices***

*Emulate, organize, burn, manage a variety of distributions for Raspberry Pi.*

- - -

### Choose your own adventure....


***Emulate:***    
`clipi` virtualizes many common sbc operating systems with QEMU.  Select from any of the included distributions (or add your own to [/sources.toml](https://github.com/Jesssullivan/clipi/blob/master/sources.toml)!) and `clipi` will handle the rest.   
        
***Organize:***    
`clipi` builds and maintains organized directories for each OS as well a [persistent & convenient .qcow2](https://www.qemu.org/docs/master/interop/qemu-img.html)  QEMU disk image.  Too many huge source *.img* files and archives?  `clipi` cleans up after itself under the ```Utilities...``` menu.

***Write:***    
`clipi` burns emulations to external disks!  Just insert a sd card or disk and follow the friendly prompts.  All files, `/home`, guest directories are written out.
- *Need to pre-configure (or double check) wifi?  Add your ssid and password to [/wpa_supplicant.conf](https://github.com/Jesssullivan/clipi/blob/master/wpa_supplicant.conf) and copy the file to `/boot` in the freshly burned disk.*     
- *Need pre-enabled ssh? copy [/ssh](https://github.com/Jesssullivan/clipi/blob/master/ssh) to `/boot` too.*

***Manage:***   
`clipi` can find the addresses of all the Raspberry Pi devices on your local network.       
- Need to do this a lot?  `clipi` can install itself as a Bash alias (option under the ```Utilities...``` menu, fire it up whenever you want.           

    
***Shortcuts:***             
Shortcuts & configuration arguments can be passed to `clipi` as a [.toml](https://github.com/toml-lang/toml) file.
- [...or you can use yaml](https://yaml.org/)                
- Supply a shortcut file like so:           
```python3 clipi.py etc/find_pi.toml```         
        

       
- take a look in [/etc](https://github.com/Jesssullivan/clipi/tree/master/etc) for some shortcut examples, here are some of mine:
   - ***write_octoprint.toml:***            
     fetches the latest octoprint image and burns it to a sd card inserted at `sdc` 
   - ***find_pi.toml:***            
     finds, prints all Raspberry Pi IPs on the local network.       
   - ***cleanup.toml:***            
     forcefully removes `/image` directory (where `clipi` builds and stores qemu emulations and disk images)
   - ***qemu_dietpi.toml:***            
     fetches and starts a buster dietpi (ARM v6) emulation.         
   - ***qemu_stretchlite.toml:***            
     fetches and starts a run-of-the-mill Raspbian stretch emulation without a desktop environment.         
   - ***qemu_stretchdesk.toml:***                            
     fetches and starts a run-of-the-mill Raspbian stretch emulation with the standard raspbian a desktop environment. 
   - ***retropie.toml:***                            
     launch a (Pi3) retropie emulator emulation *(....recursively giggles recursively....  this is a joke xD)*
                
                       
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
        
        
 <br>    
    
***`clipi` offers an interactive command line application designed to streamline the deployment of Raspberry Pi devices.  `clipi` is written in Python for Debian-based operating systems, with experimental support for Mac OS via [brew](https://brew.sh/).***
           
<br>    
        
