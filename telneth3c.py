import telnetlib
import logging
import datetime
import time
import argparse


def connect(host_ip):
    try:
        tn.open(host_ip, port=default_port)
        return True

    except:
        logging.warning('ip为%s的主机连接失败' % host_ip + '请检查网络连接')
        return False


def free_conn():
    try:
        tn.close()
    except:
        logging.warning('已断开连接')


def init_sys_argv():
    _parser = argparse.ArgumentParser()
    _parser.description = '根据以下选项输入参数：'
    _parser.add_argument('-a', '--ipaddress', help='IP地址', dest='ipaddr', type=str, default=default_host)
    _parser.add_argument('-u', '--username', help='用户', dest='account', type=str, default=default_user)
    _parser.add_argument('-p', '--password', help='密码', dest='passwd', type=str, default=default_password)
    _parser.add_argument('-f', '--filename', help='输出的文件名和路径', dest='file', type=str, default=default_path)
    return _parser


def login(user_name, pass_word):
    tn.read_until(b'Username:', timeout=5)
    print(user_name)
    tn.write(user_name.encode('ascii') + b'\n')
    tn.read_until(b'Password:', timeout=5)
    print(pass_word)
    tn.write(pass_word.encode('ascii') + b'\n')
    time.sleep(0.3)
    _result = tn.read_very_eager().decode('ascii')
    if '<10FW01-S5120-52C>' in _result:
        return True
    else:
        return False


def enter_super_mode(super_pass_word):  # 进入特权模式
    tn.write('super'.encode('ascii') + b'\n')
    time.sleep(0.2)
    tn.read_until(b' Password:', timeout=5)
    tn.write(super_pass_word.encode('ascii') + b'\n')
    time.sleep(0.2)
    _result = tn.read_very_eager().decode('ascii')

    if 'User privilege level is' in _result:

        return True

    else:
        return False


def execute_command(command):
    tn.write(command.encode('ascii') + b'\n')
    time.sleep(0.4)
    _result = tn.read_very_eager().decode('ascii')
    return _result


def deal_with_cpu_info(result_str):  # 截取过去5分钟的cpu使用率
    infolist = result_str.split('\n')
    cpu_info = ''
    for s in infolist:
        if '5 minutes' in s:
            cpu_info = s

    return cpu_info.strip()


def save_to_file(info_str, save_path):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(save_path, 'a') as f:
        f.write(info_str + "\t" + now)


default_host = "10.0.0.100"
default_user = 'gxfda'
default_password = 'wsldh@2018'
default_port = 23
default_path = 'G:\\switch\\cpu.txt'
tn = telnetlib.Telnet()
parser = init_sys_argv()
args = parser.parse_args()

if connect(args.ipaddr):
    if login(args.account, args.passwd):
        if enter_super_mode(args.passwd):
            usage = execute_command('display cpu-usage')
            result = deal_with_cpu_info(usage)
            print(result)
            save_to_file(result, args.file)
            free_conn()
        else:
            print('进入特权模式失败')
    else:
        print('登录失败，请检查用户名和密码')
else:
    print('连接失败')


