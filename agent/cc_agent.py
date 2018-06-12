#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import time
import threading
from common import UDPEndPoint
from server import STATE_UPDATE_INTERVAL


class CCAgent(UDPEndPoint):
    def __init__(self, name="Agent", port=5555, cc_server_address=None):
        self.agent_name = name
        self.cc_server = cc_server_address
        self.__heartbeat_tm = STATE_UPDATE_INTERVAL
        self.__heartbeat_thread = threading.Thread(target=self.__send_heartbeat_pkg)
        self.__is_heartbeat_thread_running = threading.Event()  # 用于停止线程的标识
        super(CCAgent, self).__init__(port=port, handler=self.recv_data_handler)

    def recv_data_handler(self, data, address):
        if self.cc_server is None:
            self.cc_server = address

        self.print_recv_data(data, address)

    def print_recv_data(self, data, address):
        print("%s收到来自%s的数据-----%s" % (self.agent_name, address, data.decode()))

    def send_state(self, state_json):
        self.send_json_to(state_json,  self.cc_server)

    def send_result(self, result_json):
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
        # self.udp_socket.shutdown(2)
        # print(self.udp_socket.getsockname())
        # print(self.udp_socket.fileno())
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


