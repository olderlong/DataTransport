#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import json
from common import UDPEndPoint
from common import event_manager, agent_event
from .agent_state_manager import AgentStateMonitor


class CCServer(UDPEndPoint):
    def __init__(self, port=8888):
        self.agent_list = []
        self.agent_state_monitor = AgentStateMonitor()
        super(CCServer, self).__init__(port=port, handler=self.receive_data_handler)

    def receive_data_handler(self, data, address):
        if address not in self.agent_list:
            self.agent_list.append(address)

        pkg_obj = dict(json.loads(str(data, encoding='utf-8')))
        try:
            if pkg_obj["Type"] == "Heartbeat":  #心跳包
                data = pkg_obj["Data"]

                agent_event.event_heartbeat.dict = data
                event_manager.send_event(agent_event.event_heartbeat)

                # self.heartbeat_handle(data)
            elif pkg_obj["Type"] == "WVSState":
                agent_event.event_wvs_state.dict = pkg_obj["WVSState"]
                print("收到代理{}的漏扫状态数据".format(address))

            elif pkg_obj["Type"] == "ScanResult":
                print("收到代理{}的漏扫结果数据".format(address))
            else:
                print("收到来自{}的未知类型数据".format(address))
        except KeyError as e:
            print("收到来自{}的未知类型数据——{}".format(address, data))

    def send_command(self, command_json):
        for address in self.agent_list:
            identifier = "[{}:{}]".format(address[0], address[1])
            if identifier in list(self.agent_state_monitor.agent_state_dict.keys()):
                self.send_json_to(command_json, address)

    def send_config(self, config_json):
        for address in self.agent_list:
            identifier = "[{}:{}]".format(address[0], address[1])
            if identifier in list(self.agent_state_monitor.agent_state_dict.keys()):
                self.send_json_to(config_json, address)
