from requests import get as r_get
from smtplib import SMTP
from email.mime.text import MIMEText as mimeT
from datetime import datetime
from getpass import getpass
import re
import subprocess

"""
Uses python 3.5+

This program checks the computers public IP and if it differs from what it knows it will send out an email to update
the user.

The program also sends out an initial email with the IP address.
"""

pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")


data = {
    'message': "Current IP address is: %s",
    'decode': 'utf-8',
    'ip page': 'https://api.ipify.org',
    'mail server': 'smtp.gmail.com',
    'username': None,
    'pass': None,
    'server id': 587,
    'timer': 60,
    'recipient': None,
    'IP': None
}


def populate_data(_data: dict)->bool:
    for item in _data:
        if item is None:
            _data[item] = _get_input(item)
        else:
            ask = _get_input("Yes or No, by entering in yes you will override %s" % item)
            if 'yes' in ask:
                _data[item] = _get_input(item)


def _get_input(d_type: str)->str:
    def __password(_data)->object:
        import base64
        return base64.b64encode(_data)
    return input("Enter in %s" % d_type) if d_type != 'pass' else _get_input(getpass("Enter in your password"))


def check_active(site: str)->bool:
    return r_get(site).status_code == 200


def send_msg(_data: dict)->bool:
    with SMTP(_data['mail server'], _data['server id']) as ser:
        if ser.starttls()[0] != 220:
            return False
        import base64
        ser.login(_data['username'], base64.b64decode(_data['pass']))
        msg = mimeT(_data['message'])
        msg['From'] = data['username']
        msg['To'] = data['recipient']
        msg['Subject'] = 'New IP address change'
        ser.sendmail(data['username'], data['recipient'], msg.as_string())
        print("Email Sent")
    return True


def main()->None:
    populate_data(data)
    last_check = datetime.now()
    while 1:
        if (datetime.now() - last_check).seconds > data['timer']:
            ip = subprocess.Popen(['curl', '-s', data['ip page']], stdout=subprocess.PIPE).communicate()
            ip = ip[0].decode(data['decode'])
            if data['IP'] != ip:
                print(ip)
                data['IP'] = ip
                send_msg(data)
            else:
                print("No Change")


if __name__ == "__main__":
    # last_check = datetime.now()
    # while 1:
    #     if (datetime.now() - last_check).seconds > __time:
    #         if check_active(_ip_webpage):
    #             global _ip
    #             ip = subprocess.Popen(['curl', '-s', _ip_webpage], stdout=subprocess.PIPE).communicate()
    #             ip = ip[0].decode(decode_type)
    #             if _ip != ip:
    #                 print(ip)
    #                 _ip = ip
    #                 send_msg(sever_name=__server, ser_num=__server_number, user=__user, password=__pass, rec=__mMail, _msg =message % ip)
    #             else:
    #                 print('No Change')
    #         last_check = datetime.now()
    main()
