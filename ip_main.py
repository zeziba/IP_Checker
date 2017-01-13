from requests import get as rGet
from smtplib import SMTP
from email.mime.text import MIMEText as mimeT
from datetime import datetime
import re
import os
import subprocess
from time import sleep

"""
Uses python 3.5+

This program checks the computers public IP and if it differs from what it knows it will send out an email to update
the user.

The program also sends out an inital email with the IP address.
"""

message = "Current IP address is: %s"

pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")

decode_type = 'utf-8'    

_ip_webpage = 'https://api.ipify.org'

__server = 'smtp.gmail.com' # if not using gmail chaing this and the sever number to required values
__user = 'empty' # Enter in own user details here
__pass = 'empty' # enter in email password
__server_number = 587

__time = 60

__mMail = 'empty' #enter in email of reciving account

_ip = None


def check_active(site: str)->bool:
    return rGet(site).status_code == 200

def send_msg(sever_name: str, serNum: int, user: str, password: str, rec: str, _msg: str)->bool:
    with SMTP(sever_name, serNum) as ser:
        if ser.starttls()[0] != 220:
            return False
        ser.login(user, password)
        msg = mimeT(_msg)
        msg['From'] = __user
        msg['To'] = __mMail
        msg['Subject'] = 'New IP adress change'
        ser.sendmail(user, rec, msg.as_string())
        print("Email Sent")
    return True


if __name__ == "__main__":
    last_check = datetime.now()
    while 1:
        if (datetime.now() - last_check).seconds > __time:
            if check_active(_ip_webpage):
                ip = subprocess.Popen(['curl', '-s', _ip_webpage], stdout=subprocess.PIPE).communicate()
                ip = ip[0].decode(decode_type)
                if _ip != ip:
                    print(ip)
                    _ip = ip
                    send_msg(sever_name=__server, serNum=__server_number, user=__user, password=__pass, rec=__mMail, _msg = message % ip)
                else:
                    print('No Change')
            last_check = datetime.now()
