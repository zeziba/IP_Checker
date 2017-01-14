#!/usr/bin/env python

from distutils.core import setup

setup(
    name="IP Automated Checker",
    version="0.5",
    description="Program automatically checks public IP address and notifies if there are any changes",
    url="http://github.com/zeziba/IP_Checker",
    author="Charles Engen",
    platforms="linux mate-debian",
    author_email="owenengen@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE V3",
    py_modules=["ip_main"],
    package_data={"", "LICENSE"},
)
