# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com
# 执行方法：python manage.py runscript onekey
# 需要安装django-extensions，pip install django-extensions

import threadpool
import datetime,time
from AutoAMS import commons
from server.models import Server
import traceback,sys
import ansible.runner,json,re

def getdata_shell(ip,user,passwd,order):

    data = ansible.runner.Runner(
        module_name = 'shell',
        module_args = order,
        remote_user = user,
        remote_pass = passwd,
        host_list = [ip],
        pattern = '',
        transport = 'smart',
        )
    try:
        data = data.run()
        data = data['contacted'][ip]
        data = data['stdout']
        result = {'status':0,'data':data}
        return result
    except Exception, e:
        print ip+" getdata_shell is Exception!!!"
        traceback.print_exc(file=sys.stdout)
        result = {'status':1,'data':'Sorry,Exception!'}
        return result


def getdata_setup(ip,user,passwd):

    data = ansible.runner.Runner(
        module_name = 'setup',
        module_args = '',
        remote_user = user,
        remote_pass = passwd,
        host_list = [ip],
        pattern = '',
        transport = 'smart',
        )
    try:
        data = data.run()
        data = data['contacted'][ip]['ansible_facts']
        result = {'status':0,'data':data}
        return result
    except Exception, e:
        print ip+" getdata_setup is Exception!!!"
        print data
        traceback.print_exc(file=sys.stdout)
        result = {'status':1,'data':'Sorry,Exception!'}
        return result

# get one server info
def get_server_info(self):

    ip = self[0]
    user = self[1]
    if(user == ''):
        user = 'root'
    passwd = self[2]
    server={}

    if(commons.myping(ip) == False):
        result = {"ip":ip,"status":"timeout","data":"ping timeout"}
        return result

    # get sn cpu server_total server_type server_model system_release system_machine
    data = getdata_setup(ip,user,passwd)

    if(data['status'] != 0):
        pass
    else:
        try:
            server_sn = str(data['data']['ansible_product_serial'])
        except Exception, e:
            server_sn = 'Unknown'

        try:
            cpu_type = str(data['data']['ansible_processor'][-1])
        except Exception, e:
            cpu_type = 'Unknown'

        try:
            cpu_total = str(data['data']['ansible_processor_vcpus'])
        except Exception, e:
            cpu_total = 'Unknown'

        try:
            server_model = str(data['data']['ansible_product_name'])
        except Exception, e:
            server_model = 'Unknown'

        try:
            server_brand = str(data['data']['ansible_system_vendor'])
        except Exception, e:
            server_brand = 'Unknown'

        try:
            system_type = str(data['data']['ansible_os_family'])
        except Exception, e:
            system_type = 'Unknown'

        try:
            system_version = str(data['data']['ansible_distribution_version'])
        except Exception, e:
            system_version = 'Unknown'

        try:
            system_machine = str(data['data']['ansible_machine'])
        except Exception, e:
            system_machine = 'Unknown'

        try:
            server_default_ipv4 = str(data['data']['ansible_default_ipv4'])
        except Exception, e:
            server_default_ipv4 = 'Unknown'

        try:
            server_all_ipv4_address = str(data['data']['ansible_all_ipv4_addresses'])
        except Exception, e:
            server_all_ipv4_address = 'Unknown'

        try:
            server_hostname = str(data['data']['ansible_hostname'])
        except Exception, e:
            server_hostname = 'Unknown'

        server['server_ip'] = ip
        server['server_sn'] = server_sn
        server['server_cpu'] = re.sub(r'\s+',' ',cpu_type)+' '+cpu_total
        server['server_model'] = server_model
        server['server_brand'] = server_brand
        server['server_system'] = system_type+' '+system_version+' '+system_machine
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
            server_memory_total = 0

            for i in range(len(size)):
                if(size[i] != 'No Module Installed'):
                    size_num = re.findall(r'(\d+) MB',str(memory['data']))
                    server_memory_total += int(size_num[0])

            memory_list.append(server_memory_total) # memory total,server['server_memory'][0]

            for i in range(len(size)):
                if(size[i] != 'No Module Installed'):
                    memory_list.append([size[i],type[i]+ip,speed[i],set[i],sn[i]])

            print server_memory_total
            print len(size)
            server['server_memory'] = json.dumps(memory_list)
        except Exception, e:
            server['server_memory'] = 'Unknown'
    if(server == {}):
        result = {"ip":ip,"status":"timeout","data":"ping is success,get serverdata is fail,please check you server's pwd"}
        return result
    else:
        result = {"ip":ip,"status":"success","data":server}
        return result

def savedata(request, result):

    if(result['status'] == "timeout"):
        print result['ip'] + ' ' + result['data']
        return "timeout"

    if 'server_sn' not in result['data']:
        print result['ip'] + ' ' + "sn error"
        return "sn error"

    server = result['data']
    sn = server['server_sn']
    print sn
    ip = server['server_ip']
    brand = server['server_brand']
    model = server['server_model']
    cpu = server['server_cpu']
    memory = server['server_memory']
    network = server['server_default_ipv4']
    all_ip = server['server_all_ipv4_address']
    system = server['server_system']
    hostname = server['server_hostname']
    user = 'system'
    status = 'product'

    # 如果序列号已经存在，只做更新
    if Server.objects.filter(sn = sn):

        olddata = Server.objects.filter(sn = sn)
        id = olddata[0].id

        server_update = Server.objects.get(id = id)
        server_update.ip = ip
        server_update.brand = brand
        server_update.model = model
        server_update.cpu = cpu
        server_update.memory = memory
        server_update.network = network
        server_update.all_ip = all_ip
        server_update.system = system
        server_update.hostname = hostname
        server_update.user = user
        server_update.status = status
        server_update.save()

        print ip+' is update >>>>'
        return "update"
    # 插入数据库
    server_add = Server(
        sn = sn,
        ip = ip,
        brand = brand,
        model = model,
        cpu = cpu,
        memory = memory,
        network = network,
        all_ip = all_ip,
        system = system,
        hostname = hostname,
        user = user,
        status = status,
        )

    server_add.save()

    print ip+' is add ****'
    return "add"

def run_threadpool(maxthread,datalist):
    try:
        pool = threadpool.ThreadPool(maxthread) # 定义最大线程数
        starttime = 'pro start %s' % datetime.datetime.now()

        requests = threadpool.makeRequests(get_server_info, datalist, savedata)
        [pool.putRequest(req) for req in requests]
        pool.wait()

        endtime = 'pro end %s' % datetime.datetime.now()
        print starttime,endtime
        return  True
    except Exception, e:
        print "The program failed to run, please try again."
        traceback.print_exc(file=sys.stdout)
        return False

def run():
    # list格式：[["192.168.1.100", "root", "123456"],]
    datalist = json.loads(open('/root/hostlist.json').read())
    datalist = [
        ['192.168.216.102','root',''],
    ]

    maxthread = 20 #最大开启线程数
    run_threadpool(maxthread,datalist) # 执行多线程函数

