# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com
# 执行方法：python manage.py runscript onekey
# 需要安装django-extensions，pip install django-extensions


import datetime
import os
import threading
import time

import ansible.runner,json,re


def getdata_shell(ip,user,passwd,order):
    hosts = [ip]
    data = ansible.runner.Runner(
        module_name = 'shell',
        module_args = order,
        remote_user = user,
        remote_pass = passwd,
        host_list = hosts,
        pattern = '',
        )
    try:
        data = data.run()
        data = data['contacted'][ip]
        data = data['stdout']
        result = {'status':0,'data':data}
        return result
    except Exception, e:
        result = {'status':1,'data':'Sorry,Exception!'}
        return result


def getdata_setup(ip,user,passwd):
    hosts = [ip]
    data = ansible.runner.Runner(
        module_name = 'setup',
        module_args = '',
        remote_user = user,
        remote_pass = passwd,
        host_list = hosts,
        pattern = '',
        )
    try:
        data = data.run()
        data = data['contacted'][ip]['ansible_facts']
        result = {'status':0,'data':data}
        return result
    except Exception, e:
        result = {'status':1,'data':'Sorry,Exception!'}
        return result



# get one server info

def get_server_info(ip,user,passwd):

    server={}
    # get sn cpu server_total server_type server_model system_release system_machine
    data = getdata_setup(ip,user,passwd)
    if(data['status'] != 0):
        pass
    else:
        try:
            sn = str(data['data']["ansible_product_serial"])
        except Exception, e:
            sn = "Unknown"

        try:
            cpu_type = str(data['data']["ansible_processor"][-1])
        except Exception, e:
            cpu_type = "Unknown"

        try:
            cpu_total = str(data['data']["ansible_processor_vcpus"])
        except Exception, e:
            cpu_total = "Unknown"

        try:
            server_type = str(data['data']["ansible_product_name"])
        except Exception, e:
            server_type = "Unknown"

        try:
            server_model = str(data['data']["ansible_system_vendor"])
        except Exception, e:
            server_model = "Unknown"

        try:
            system_type = str(data['data']["ansible_os_family"])
        except Exception, e:
            system_type = "Unknown"

        try:
            system_release = str(data['data']["ansible_lsb"]["release"])
        except Exception, e:
            system_release = "Unknown"

        try:
            system_machine = str(data['data']["ansible_machine"])
        except Exception, e:
            system_machine = "Unknown"

        try:
            server_default_ipv4 = str(data['data']["ansible_default_ipv4"])
        except Exception, e:
            server_default_ipv4 = "Unknown"

        try:
            server_all_ipv4_address = str(data['data']["ansible_all_ipv4_addresses"])
        except Exception, e:
            server_all_ipv4_address = "Unknown"

        try:
            server_hostname = str(data['data']["ansible_hostname"])
        except Exception, e:
            server_hostname = "Unknown"






        server['server_sn'] = sn
        server['server_cpu'] = re.sub(r'\s+',' ',cpu_type)+" "+cpu_total
        server['server_type'] = server_type
        server['server_model'] = server_model
        server['server_system'] = system_type+" "+system_release+" "+system_machine
        server['server_hostname'] = server_hostname
        server['server_default_ipv4'] = json.dumps(server_default_ipv4)
        server['server_all_ipv4_address'] = json.dumps(server_all_ipv4_address)

    # get memory disk,use dmidecode
    memory = getdata_shell(ip,user,passwd,'dmidecode -t memory')
    if(memory['status'] != 0):
        pass
    else:
        try:
            size=re.findall(r'\n\s+Size: (.*)\n',str(memory['data']))
            type=re.findall(r'\n\s+Type: (.*)\n',str(memory['data']))
            speed=re.findall(r'\n\s+Speed: (.*)\n',str(memory['data']))
            set=re.findall(r'\n\s+Set: (.*)\n',str(memory['data']))
            sn=re.findall(r'\n\s+Serial Number: (.*)\n',str(memory['data']))

            memory_list = []
            memory_item = []
            for i in range(len(size)):
                if(size[i] != 'No Module Installed'):
                    memory_list.append([size[i],type[i],speed[i],set[i],sn[i]])

            server['server_memory'] = json.dumps(memory_list)
        except Exception, e:
            server['server_memory'] = "Unknown"
    print server
    return server


def run():
    iplist = [
        ['192.168.1.101','root',''],


       ]

    threads = []

    starttime = "pro start %s" % datetime.datetime.now()

    for ip in iplist:
        th = threading.Thread(target=get_server_info, args=(ip[0],ip[1],ip[2]))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    endtime = "pro end %s" % datetime.datetime.now()
    print starttime,endtime
    return  starttime+"<br>"+endtime

