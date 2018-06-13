#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import shutil
import logging
import subprocess
from agent import WVSControlBase

logger = logging.getLogger("Agent")


class AppScanControl(WVSControlBase):
    def __init__(self):
        self.appscan_path = "appscancmd.exe"
        super(AppScanControl, self).__init__()

    def start_new_scan(self, config):
        """
        开始一个新的扫描，首先提取扫描配置参数，主要包括起始URL、扫描策略；其次基于StartURL创建扫描项目目录，copy配置文
        件到该目录，针对APPScan 用StartURL替换扫描配置模板模板中的StartUrl， 生成结果文件名等参数；最后构造命令行参数，
        启动扫描
        :param config:
        :return:
        """
        self.start_url = config["StartURL"]
        scan_policy = config["ScanPolicy"]
        logger.info("Start a scan to website <{}> with a policy <{}>".format(self.start_url, scan_policy))
        self.__create_scan_project_dir(self.start_url)

        self.__init_scan_config()

        self.appscan_shell_cmd = "{} /e /st {} /su {} /d {} /rt xml /rf {}".format(
            self.appscan_path,
            self.scan_template_file,
            self.start_url,
            self.scan_result_file,
            self.scan_result_xml_file
        )
        logger.info("Appscan shell command is: {}".format(self.appscan_shell_cmd))
        # for debug
        self.appscan_shell_cmd = "ping -n 15 www.baidu.com"
        # for debug
        self.__start_appscan(self.appscan_shell_cmd)


    def stop_scan(self):
        print("stop")

    def __start_appscan(self, cmd):
        self.appscan_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while self.appscan_process.poll() is None:
            line = self.appscan_process.stdout.readline()
            line_str = str(line, 'gbk')
            line_str = line_str.strip()
            if line_str:
                print("Appscan扫描进程输出：{}".format(line_str))

        if self.appscan_process.returncode == 0:
            logger.info("Appscan扫描进程成功结束")
        else:
            logger.error("Appscan扫描进程运行失败：{}".format(self.appscan_process.returncode))


    def __init_scan_config(self):
        """
        根据配置信息，修改扫描模板文件
        :return:
        """
        pass

    def __create_scan_project_dir(self, start_url):
        hostname = start_url.split("//")[1].split("/")[0]
        self.current_dir = os.getcwd()
        self.scan_project_dir = os.path.join(self.current_dir, "scan_project", hostname)
        if not os.path.exists(self.scan_project_dir):
            os.makedirs(self.scan_project_dir)
            logger.info("扫描项目目录>>{}\t创建成功".format(self.scan_project_dir))
        else:
            logger.info("扫描项目目录>>{}\t已存在".format(self.scan_project_dir))

        self.scan_result_file = os.path.join(self.scan_project_dir, hostname + ".scan")
        if os.path.exists(self.scan_result_file):
            os.remove(self.scan_result_file)

        self.scan_result_xml_file = os.path.join(self.scan_project_dir, "result.xml")
        if os.path.exists(self.scan_result_xml_file):
            os.remove(self.scan_result_xml_file)

        self.scan_template_file = os.path.join(self.scan_project_dir, "base.scant")
        if os.path.exists(self.scan_template_file):
            os.remove(self.scan_template_file)

        self.__gen_scan_template_file()

    def __gen_scan_template_file(self):
        source_file = os.path.join(os.getcwd(), "base.scant")
        if os.path.exists(source_file):
            if not os.path.exists(self.scan_template_file):
                shutil.copy(source_file, self.scan_template_file)
            else:
                logger.error("扫描项目中模板文件已经存在")
        else:
            logger.error("模板文件不存在")




