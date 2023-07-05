import requests
import json
import os,time,sys,re,datetime
import paramiko
import alarm,os

def execute_remote_command(hostname, port,host_miner, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if output:
            print(f"=== Output from {hostname} ===")
            print(host_miner)
            print(output)
            test_007_robot(output)
        if error:
            print(f"=== Error from {hostname} ===")
            print(host_miner)
            print(error)
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {hostname}.")
    except paramiko.SSHException as e:
        print(f"SSH connection error: {str(e)}")
    finally:
        client.close()






def get_filscout():
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36", "Content-Type": "text/plain"}
    url = 'https://api2.filscout.com/api/v1/message'
    data = {"address":"","blockCid":"","exitCode":"","idAddress":"","method":"PublishStorageDeals","pageIndex":1,"pageSize":20,"timeEnd":0,"timeStart":0}
    r = requests.post(url, headers=headers, json=data)
    r_dic = eval(r.text.replace("null", "0"))
    gas_t_str = ''
    T_gas_list = []
    for i in range(10):
        cid = r_dic['data'][i]['cid']
        tmp,T_gas = gas_t(cid)
        T_gas_list.append(T_gas)
        gas_t_str +=  tmp
    print(T_gas_list)
    float_list = [float(num) for num in T_gas_list]
    total = sum(float_list)
    length = len(float_list)
    average = total / length
    average_rounded = round(average, 2)
    print(average_rounded)
    # 比较3.5和average_rounded
    if 2.8 > average_rounded:
        msg_tmp = '最近10个订单真实数据导入小于2.8FIl/T尽快导入订单,准备启动自动导入订单'
        print(msg_tmp)
        cmd_ssh() 
        test_007_robot(msg_tmp)
    elif 2.8 < average_rounded:
        msg_tmp = '最近10个订单真实数据导入大于2.8FIl/T不能导入订单'
        print(msg_tmp)
        test_007_robot(msg_tmp)
    else:
        print("3.5 等于平均数")
    test_007_robot(gas_t_str)

def gas_t(cid):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36", "Content-Type": "text/plain"}
    url_m = 'https://api2.filscout.com/api/v1/message/{}'.format(cid)
    data_m = {}
    r_m = requests.get(url_m, headers=headers, json=data_m)
    r_dic_m = r_m.text.replace("null", "0")
    r_dic_m = json.loads(r_dic_m)
    now_time = r_dic_m['data']['time']
    totalBurnFee = r_dic_m['data']['totalBurnFee']
    quantity = r_dic_m['data']['return']  
    quantity = json.loads(quantity)
    quantity = quantity['ValidDeals'][-1]
    #print(cid)
    #print(totalBurnFee)
    try:
        totalBurnFee = float(re.sub(r'\s+FIL', '', totalBurnFee))
        #print(totalBurnFee)
    except Exception as e:
        print("nanoFIL")
        totalBurnFee = totalBurnFee.replace(',', '')
        totalBurnFee = float(re.sub(r'\s+nanoFIL', '', totalBurnFee))
        totalBurnFee = totalBurnFee / 1000000000
    T_gas = totalBurnFee/int(quantity) * 32
    T_gas = "%.4f" % T_gas
    tmp = "当前时间：{}\t每T销毁gas：{} Fil\t真实数据订单数量：{}\n".format(now_time,T_gas,quantity)
    return tmp,T_gas 

def test_007_robot(msg_info):
   headers = {"Content-Type": "text/plain"}
   now_time = datetime.datetime.now().replace(microsecond=0)
   s = msg_info
   #print(now_time,s)
   #print(s)
   data = {
      "msgtype": "text",
      "text": {
         "content": s,
      "mentioned_list": [""]
      }
    }
   r = requests.post(
         url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=47b8cab0-ad26-4879-b7e9-965abb555105',
         headers=headers, json=data)
   print(r.text)

def cmd_ssh():
    # 远程机器的IP地址和端口
    miner_dic = {"f01656666":["172.25.5.70","22"],"f02229760":["172.25.5.43","22"]}
    #miner_dic = {"f01656666":["172.25.5.70","22"],"f01530777":["103.90.153.194","236"],"f02229760":["172.25.5.43","22"]}
    #miner_dic = {"f01656666":["172.25.5.70","22"]}

    command = '''unset GOLOG_LOG_LEVEL && bash   /root/auto-dc.sh'''

    # 格式化当前时间
    for host in miner_dic:
        execute_remote_command(miner_dic[host][0],miner_dic[host][1],host,command)

if __name__ == '__main__':
    get_filscout()
