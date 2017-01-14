#!/usr/bin/env python

from requests import get as r_get
from smtplib import SMTP
from email.mime.text import MIMEText as mimeT
from datetime import datetime
from getpass import getpass
import subprocess

"""
Created By: Charles Engen   1/13/2017

This program asks for information on an account to use as a email host and an email recipient. After
collecting this data the program will proceed to check the public IP address, if there is a change detected
the program will use the supplied email address to send an email about the change in the IP address.

The purpose of this program is to make it so that my home computer can be easily found on the web so that
I can use it as a server with out a static IP address. So even if it changes I will still have access to the
material and content that is required.
"""


data = {
    'message': "Current IP address is: %s",
    'decode': 'utf-8',
    'ip page': 'https://api.ipify.org',
    'mail server': 'smtp.gmail.com',
    'username': None,
    'pass': None,
    'server id': 587,
    'timer': 1,
    'recipient': None,
    'IP': "",
    'start': False
}


def populate_data(_data: dict)->bool:
    """
    This function populates the data with all the necessary information
    :param _data: dict object containing the necessary data
    :return: if function passed, a True value is returned
    """

    def _get_input(d_type: str)->str:
        """
        Function is an internal function that get the user input and returns it, there will be checking
        added later.
        :param d_type:
        :return:
        """
        return input("Enter in %s:" % d_type).lower() if d_type != 'pass'\
            else str(getpass("Enter in your password"))

    m_ask = input("Would you like o override the defaults? Enter Yes or No:\n")
    for key, item in _data.items():
        if item is None:
            _data[key] = _get_input(key)
        elif 'Yes' in m_ask.lower():
            ask = _get_input("Yes or No, by entering in yes you will override: %s" % item)
            if 'yes' in ask:
                _data[key] = _get_input(key)
    return True


def check_active(site: str)->bool:
    """
    Function checks the state of a webpage to see if it is able to be accessed.
    :param site: give a string of the webpage including the http://
    :return: completion status
    """
    return r_get(site).status_code == 200


def send_msg(_data: dict)->bool:
    """
    Function sends an email with the supplied credentials
    :param _data: data dictionary that has the requested data
    :return: status code if the email was sent or not, True or False
    """
    with SMTP(_data['mail server'], _data['server id']) as ser:
        if ser.starttls()[0] != 220:
            return False
        ser.login(_data['username'], _data['pass'])
        msg = mimeT(_data['message'] % data['IP'])
        msg['From'] = data['username']
        msg['To'] = data['recipient']
        msg['Subject'] = 'New IP address change'
        ser.sendmail(data['username'], data['recipient'], msg.as_string())
        print("Email Sent")
    return True


def main()->None:
    """
    The main loop of the program
    :return: should not return any value
    """

    def __populate_mail()->None:
        """
        internal function to populate the message and send it
        :return: nothing is returned
        """
        ip = subprocess.Popen(['curl', '-s', data['ip page']], stdout=subprocess.PIPE).communicate()
        ip = ip[0].decode(data['decode'])
        if data['IP'] != ip:
            print(ip)
            data['IP'] = ip
            send_msg(data)
        else:
            print("No Change")

    populate_data(data)
    last_check = datetime.now()

    while 1:
        if not data['start']:
            data['start'] = True
            __populate_mail()
        if (datetime.now() - last_check).seconds > data['timer']:
            __populate_mail()


if __name__ == "__main__":
    main()
