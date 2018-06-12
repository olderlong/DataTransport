#! /usr/bin/env python
# _*_ coding:utf-8 _*_
from agent import WVSControlBase

class AppScanControl(WVSControlBase):
    def __init__(self):

        super(AppScanControl, self).__init__()

    def start_new_scan(self, config):
        start_url = config["StartURL"]
        scan_policy = config["ScanPolicy"]
        print("Start a scan to website <{}> with a policy <{}>".format(start_url, scan_policy))

    def stop_scan(self):
        print("stop")