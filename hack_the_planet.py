#!/usr/bin/env python

# This code was written 10 hours before the competition, yikes
# Any bugs are your problem

import socks # pip install PySocks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
socket.socket = socks.socksocket

from pwn import * # pip install pwntools
from swpag_client import Team # pip install swpag_client
import time

team = Team(None, "Team_Key_Here")

def team_ip(team_host):
    # 172.31.129.1 (team1) ... 172.31.129.254 (team254) ... 172.31.130.1 (team255) ...
    team_number = int(team_host[4:])
    minor = ((team_number - 1) % 254) + 1
    major = (team_number / 255) + 129
    return '172.31.{major}.{minor}'.format(major=major, minor=minor)

services = team.get_service_list()
service_flag_ids = dict()

while True:
    for service in services:
	if service['service_name'] != 'babymarvel':
		continue
        print("Going to attack", service['service_name'])
        if service['service_name'] not in service_flag_ids:
            service_flag_ids[service['service_name']] = set()
        targets = team.get_targets(service['service_id'])
#        for target in targets['targets']:
	for target in targets:
            flag_id = target['flag_id']
            ip = team_ip(target['hostname'])
            port = target['port']
            print ip, port, flag_id
            if flag_id not in service_flag_ids[service['service_name']]:
                try:
                    conn = remote(ip, port, timeout=3)
                    # insert pwnage here
                    conn.close()
                    flag = "GET_THE_FLAG"
                    # result = team.submit_flag(flag)
                    # print(result)
                    print("HACKED")
                except Exception as e:
                    print("Error connecting to", target['team_name'], target['hostname'], ip, port)
                    print(e)
                service_flag_ids[service['service_name']].add(flag_id)

    time.sleep(10) # DOS is against the rules

