#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import time
import threading
import json
import logging
from common import UDPEndPoint, event_manager, agent_event
from server import STATE_UPDATE_INTERVAL

logger = logging.getLogger("Agent")


class CCAgent(UDPEndPoint):
    def __init__(self, name="Agent", port=5555, cc_server_address=None):
        self.agent_name = name
        self.cc_server = cc_server_address
        self.__heartbeat_tm = STATE_UPDATE_INTERVAL
        self.__heartbeat_thread = threading.Thread(target=self.__send_heartbeat_pkg)
        self.__is_heartbeat_thread_running = threading.Event()  # 用于停止线程的标识

        # self.EVENT_SCAN_RESULT_SEND = "SendResultSend"
        # self.event_scan_result_send = Event(type_=self.EVENT_SCAN_RESULT_SEND)
        event_manager.add_event_listener(agent_event.EVENT_SCAN_RESULT_SEND, self.send_result)

        super(CCAgent, self).__init__(port=port, handler=self.recv_data_handler)

    def recv_data_handler(self, data, address):
        if self.cc_server is None:
            self.cc_server = address

        pkg_obj = dict(json.loads(str(data, encoding='utf-8')))
        #针对Data中字段进行分析处理
        try:
            if pkg_obj["Type"] == "WVSCommand":  #命令数据包
                data = pkg_obj["Data"]
                agent_event.event_wvs_command.dict = data
                event_manager.send_event(agent_event.event_wvs_command)
            elif pkg_obj["Type"] == "AgentControl":
                data = pkg_obj["Data"]
                if data["Control"] == "Exit":
                    agent_event.event_agent_exit.dict = data
                    event_manager.send_event(agent_event.event_agent_exit)
                    logger.info("Agent exit...")
            else:
                logger.info("收到来自{}的未知类型数据".format(address))
        except KeyError as e:
            logger.error("收到来自{}的未知类型数据——{}".format(address, data))

    def send_state(self, state_json):
        self.send_json_to(state_json,  self.cc_server)

    def send_result(self, event):
        result_json = event.dict
        self.send_json_to(result_json, self.cc_server)
        
    def start(self):
        self.__start_heartbeat()
        super(CCAgent, self).start()

    def __start_heartbeat(self):
        self.__is_heartbeat_thread_running.set()
        # self.__heartbeat_tm = delay
        self.__heartbeat_thread.daemon = True
        self.__heartbeat_thread.start()

    def stop(self):
        # event_manager.stop()
        self.__is_heartbeat_thread_running.clear()
        super(CCAgent, self).stop()

    def __send_heartbeat_pkg(self):
        while self.__is_heartbeat_thread_running:
            state = {
                "Type": "Heartbeat",
                "Data": {
                    "Name":  self.agent_name,
                    "Address":  self.address,
                    "Timestamp":  time.time(),
                    "State":  "Online"
                }
            }
            self.send_state(state)
            time.sleep(self.__heartbeat_tm)


