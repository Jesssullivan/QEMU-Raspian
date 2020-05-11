from netifaces import gateways
from sys import argv
import time
import subprocess
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import head, status_codes
import re



interval = .25


def rand_hex(l: int, return_string=''):
    for char in range(l):
        return_string = return_string + (random.choice("0123456789ABCDEF"))
    return return_string


def newmac():
    mac = ''
    for pair in range(5):
        mac += rand_hex(2) + ':'
    mac += rand_hex(2)
    return mac


def is_loaded(url):
    count = 0
    r = head(url)
    for X in range(10):
        if r.status_code != 200:
            time.sleep(interval)
            count += interval
            print('loading page, waited ' + str(count) + ' secs... ')
            if X == 10:
                raise SystemExit
        elif r.status_code == 200:
            print("url loaded!")
            return True


def argtype():
    try:
        if len(argv) > 1:
            use = True
        elif len(argv) == 1:
            use = False
        else:
            print('command takes 0 or 1 args, use -h for help')
            raise SystemExit
    except:
        print('arg error... \n command takes 0 or 1 args, use -h for help')
        raise SystemExit
    return use


def gate():
    all_gates = gateways()
    try:
        target = all_gates['default'][2][0]
    except:
        print('gateway error! please make sure a network is available')
    return target



driver = webdriver.Chrome(os.path.abspath('chromedriver'))  # Optional argument, if not specified will search path.
curgate = gate()
cururl = 'http://' + curgate + '/'
driver.get(str('http://' + curgate + '/'))

"""

sudo ifconfig wlp3s0 down
sudo ifconfig wlp3s0 hw ether 00:11:22:33:44:55
sudo ifconfig wlp3s0 up
"""


def commitMAC():
    subprocess.Popen(
        str('ifconfig wlp3s0 down && sleep .25 ' +
            '&& sudo ifconfig wlp3s0 hw ether ' + newmac() +
            ' sleep .25 && sudo ifconfig wlp3s0 up'),
        shell=True,
        executable='/bin/bash')


id_list = [
    "amdocs_signup",
    "continueButton",
    "banner_green_text",
    "get_started_button",
    "signUpButton",
    "upgradeOfferCancelButton",
    "offersFreeList1",
]

for x in range(10):
    if str(driver.current_url).startswith('https://login.'):
        commitMAC()
        time.sleep(.1)
        continue
    for ids in id_list:
        if is_loaded(driver.current_url):
            try:
                u = driver.find_element_by_id(ids)
                u.click()
            except:
                time.sleep(.25)


https://login.xfinity.com/login?r=comcast.net&s=oauth&continue=https%3A%2F%2Foauth.xfinity.com%2Foauth%2Fauthorize%3Flogin_hint%3D2003airmax3%26macId%3D00%253A11%253A22%253A33%253A44%253A56%26response_type%3Dcode%26client_id%3Dwifi-on-demand%26redirect_uri%3Dhttps%253A%252F%252Fwifiondemand.xfinity.com%252Fwod%252Flanding%26scope%3Dopenid%26response%3D1&ruid=2003airmax3&client_id=wifi-on-demand&reqId=127022ed-6278-4170-bab1-fb5b7f618d94
S = driver.find_element_by_id("continueButton")
S.click()

https://wifiondemand.xfinity.com/wod/landing?c=n&macId=00%3A11%3A22%3A33%3A44%3A55&a=as&bn=st22&location=Outdoor&apMacId=74%3Aea%3Ae8%3Af2%3Aad%3Aea&issuer=r&deviceModel=Linux+Chrome+-+Linux&NASIP=68.86.15.187&deviceName=default&deviceName=default
Next('')
Next("get_started_button")
Next("offersFreeList1")
Next("continueButton")
Next("upgradeOfferCancelButton")
Next("upgradeOfferCancelButton")
Next("signUpButton")

    N1 = rand_string(8)
    FName = driver.find_element_by_id("firstName")
    FName.send_keys(N1)

    N2 = rand_string(8)
    LName = driver.find_element_by_id("lastName")
    LName.send_keys(N2)

    N3 = rand_string(8)
    UName = driver.find_element_by_id("userName")
    UName.send_keys(N3)

    EMail = driver.find_element_by_id("alternateEmail")
    EMail.send_keys(N1 + '@' + N2 + '.com')

    SQ = driver.find_element_by_id("dk0-combobox")
    SQ.send_keys(Keys.ARROW_DOWN)

    N4 = rand_string(5)
    SA = driver.find_element_by_id("secretAnswer")
    SA.send_keys(N4)

    N5 = str(rand_string(9) + '1!')
    pwd = driver.find_element_by_id("password")
    pwd.send_keys(N5)
    repwd = driver.find_element_by_id("passwordRetype")
    repwd.send_keys(N5)

    time.sleep(10)
    submit = driver.find_element_by_id("submitButton")
    submit.click()

    time.sleep(10)
    activate = driver.find_element_by_id("_orderConfirmationActivatePass")
    activate.click()
