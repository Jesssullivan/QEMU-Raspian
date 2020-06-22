# Using QEMU for Raspian ARM         
     
*single ARM guest configuration tested on Mac OSX 10.14.6 host*        
*experimental multi-guest support for Ubuntu 18.04 host (Gnome / Budgie) over virtual network bridge*    

    
Emulates a variety of Raspian releases on proper ARM hardware with QEMU.  

***Prerequisites:***    

QEMU and wget (OSX homebrew)

```bash
# OSX:
brew install qemu wget 

# Ubuntu:
sudo apt-get install qemu-system-arm -y
```      

Get the Python3 CLI in this repo:
```bash
wget https://raw.githubusercontent.com/Jesssullivan/USBoN/master/QEMU_Raspian.py
```  
- - -

***info - multiple guests over virtual bridge (.deb distros only):***                       

- multiple guests get unique MAC addresses  
- see /setupHostDepends.sh for required packages    
    
```bash

# permiss shell scripts with ``` sudo chmod u+x ... ``` 

sudo ./setupHostDepends.sh

# switch to bridge br0:
sudo ./UPbrctl.sh

# back to normal host network:
sudo ./DOWNbrctl.sh

# add network bits for host:
rm /etc/network/interfaces  # existing lo file
cp interfaces /etc/network/  # replace from this repo
cp qemu-ifup /etc/

```     

- - -
***usage - single guest:***               

After the first launch, it will launch from the persistent .qcow2 image.         

With no arguments & in a new folder, Raspian "stretch-lite" (no desktop environment) will be:        
    - downloaded as a zip archive with a release kernel      
    - unarchived --> to img      
    - converted to a Qcow2 with 8gb allocated as disk        
    - launched from Qcow2 as administrator       
     
```bash
sudo python3 QEMU_Raspian.py 
```             
 
***optional guest configuration arguments:***       
    
-  ``` -h ```  prints CLI usage help         
- ``` -rm ``` removes ALL files added in dir with QEMU_Raspian.py        
- ``` stretch ``` uses standard graphical stretch release with GUI        
- ```stretchlite ``` for stretchlite release [default!]          
- ``` buster ``` for standard graphical buster release [YMMV]     
- ```busterlite``` for busterlite release [YMMV]            
    
```bash
# examples:
sudo python3 QEMU_Raspian.py busterlite
python3 QEMU_Raspian -h  # print help
```
     
- - -     

```
# YMMV: burn / backup as .img:     

to burn the new image back to an SD card for a hardware Pi:     

# bash
qemu-img convert -f qcow2 -O raw file.qcow2 file.img
```  
- - -

![Alt text](imgs.png?raw=true)
