#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import os, shutil,logging
from agent import WVSControlBase


class AppScanControl(WVSControlBase):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        super(AppScanControl, self).__init__()

    def start_new_scan(self, config):
        """
        开始一个新的扫描，首先提取扫描配置参数，主要包括起始URL、扫描策略；其次基于StartURL创建扫描项目目录，copy配置文
        件到该目录，针对APPScan 用StartURL替换扫描配置模板模板中的StartUrl， 生成结果文件名等参数；最后构造命令行参数，
        启动扫描
        :param config:
        :return:
        """
        start_url = config["StartURL"]
        scan_policy = config["ScanPolicy"]
        print("Start a scan to website <{}> with a policy <{}>".format(start_url, scan_policy))
        self.__create_scan_project_dir(start_url)




    def stop_scan(self):
        print("stop")

    def __create_scan_project_dir(self, start_url):
        hostname = start_url.split("//")[1].split("/")[0]
        self.current_dir = os.getcwd()
        self.scan_project_dir = os.path.join(self.current_dir, "scan_project", hostname)
        if not os.path.exists(self.scan_project_dir):
            os.makedirs(self.scan_project_dir)
            print(self.scan_project_dir)

            self.scan_result_file = os.path.join(self.scan_project_dir, hostname+".scan")
            self.scan_result_xml_file = os.path.join(self.scan_project_dir, "result.xml")
            self.scan_template_file = os.path.join(self.scan_project_dir, "base.scant")
            self.__gen_scan_template_file()
        else:

    def __gen_scan_template_file(self):
        source_file = os.path.join(os.getcwd(), "base.scant")
        if os.path.exists(source_file):
            if not os.path.exists(self.scan_template_file):
                shutil.copy(source_file, self.scan_template_file)
            else:
                logging.error("扫描项目中模板文件已经存在")
        else:
            logging.error("模板文件不存在")




