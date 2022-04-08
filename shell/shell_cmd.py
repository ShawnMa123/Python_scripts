import subprocess
import os
import re
from typing import *

class Cmd:
    '''
    包含一些常用命令行操作，比如查看路由表，查看ipv4网关，ping
    '''
    def get_all_route():
        '''
        查看本地所有路由表
        无需参数
        :return:
        '''
        sys_route_table = os.popen('route print')
        sys_route_table_res = sys_route_table.read()
        print(sys_route_table_res)


    def get_ipconfig():
        '''
        获取本地ipv4网关信息
        无需参数
        :return: 会返回一个ipv4地址的list，比如[[192.168.100.1]]
        '''
        sys_ipconfig = os.popen('ipconfig')
        ipconfig_res = sys_ipconfig.read()
        ipconfig_res_list = ipconfig_res.splitlines()

        # 获取包含默认网关字段的所有输出，并且ipv4地址中一定包含数字，用于筛选
        gateway_list = []
        for x in ipconfig_res_list:
            if '默认网关' in x and bool(re.search(r'\d', x)):
                gateway_list.append(x)
        # print(gateway_list)

        # 目前大部分ont的网关地址都是ipv4，所以进行ipv4的筛选
        getway_ipv4_address_list = []
        for x in gateway_list:
            gateway_ipv4_ip = re.findall(r"\d+\.\d+\.\d+\.\d+", x)
            getway_ipv4_address_list.append(gateway_ipv4_ip)
        for x in getway_ipv4_address_list:
            print(f'网关ipv4地址为 {x[0]}')
        return getway_ipv4_address_list

    def ping_client(ip: str, times: int) -> bool:
        '''
        用来ping给定的ip地址，返回是否能ping通。在第一次无法ping通的时候，会自动再ping10次。
        :param ip: ping ip
        :param times: ping 次数
        :return:
            True: 可以ping通
            False: 无法ping通
        '''
        # 第一次ping多给点耐心，多加ping5次
        ping_cmd = "ping " + ip + " -n " + str(5+times)
        sys_ping = os.popen(ping_cmd)

        # 一般来说，如果ping通的话，系统会显示  “数据包: 已发送 = 10，已接收 = 10，丢失 = 0 (0% 丢失)，”，根据里面的0%来匹配
        if "0%" in sys_ping.read():
            print(f'ping {ip} succeed')
            return True
        else:
            # 不行的话需要再ping10次，这时已经至少ping了15次，如果还是不通，建议检查其他项目
            sys_ping = os.popen("ping " + ip + " -n 10")
            if "0%" not in sys_ping.read():
                print(f'ping {ip} failed after 10 times')
                return False


if __name__ == '__main__':
    Cmd.get_all_route()
    Cmd.get_ipconfig()
    res = Cmd.ping_client('192.168.50.1', 5)

