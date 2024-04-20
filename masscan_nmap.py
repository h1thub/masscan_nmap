import nmap
import json
import os
from multiprocessing import Pool, Manager

# 全局变量定义区域
ip_file = 'ips.txt' # IP地址列表文件
masscan_exe = '/opt/homebrew/bin/masscan'   # masscan程序的路径
masscan_rate = 2000 # masscan 扫描的速率，单位为每秒发送的包数
masscan_file = 'masscan_results.json'   # masscan的输出结果文件
process_num = 50  # 进程池中进程的数量，用于并行处理任务

def run_masscan():
    # 该函数构建并执行masscan命令，扫描指定的IP范围，输出结果为JSON格式
    command = f'sudo {masscan_exe} -iL {ip_file} -p 1-65535 -oJ {masscan_file} --rate {masscan_rate}'
    os.system(command)  # 使用系统调用执行构建的命令

def extract_masscan():
    # 该函数从masscan的输出文件中提取扫描结果，返回一个任务列表
    task_list = []
    try:
        with open(masscan_file, 'r') as fr:
            data = json.load(fr)    # 加载JSON数据
        # 删除每个扫描结果的 timestamp 字段
        for item in data:
            if 'timestamp' in item:
                del item['timestamp']  # 删除 timestamp 字段
        # 将修改后（删除timestamp字段）的数据写回文件
        with open(masscan_file, 'w') as fw:
            json.dump(data, fw, indent=4)
        # 生成任务列表
        for item in data:   # 遍历每一个扫描结果项
            ip = item['ip'] # 获取IP地址
            ports = item['ports']   # 获取端口信息列表
            for port in ports:  # 遍历端口列表
                task_list.append(f"{ip}:{port['port']}")    # 构造ip:port格式的字符串，添加到任务列表
        return task_list
    except json.JSONDecodeError:
        print("masscan_results.json is empty or malformed.")    # 文件为空或格式错误
        return task_list
    except Exception as e:
        print(f"Error extracting masscan results: {e}") # 打印其他异常信息
        return task_list

def nmap_scan(ip_port):
    # 该函数使用nmap扫描单个ip:port，返回服务信息
    ip, port = ip_port.split(':')   # 分解获取IP和端口号
    try:
        nm = nmap.PortScanner() # 创建PortScanner对象
        nm.scan(ip, port, arguments='-Pn -sS')  # 执行nmap扫描
        service = nm[ip]['tcp'][int(port)]['name']  # 获取服务名称
        return f"{ip}:{port}:{service}" # 返回格式化的扫描结果
    except Exception as e:
        return f"Error scanning {ip_port}: {e}" # 错误处理，返回错误信息

def run_nmap(task_list):
    # 该函数使用多进程对提取的任务列表进行nmap扫描
    with Pool(process_num) as pool: # 创建进程池
        results = pool.map(nmap_scan, task_list)    # 对每个任务应用nmap_scan函数
    return results

def save_results(results):
    # 该函数将nmap扫描结果保存到文件
    with open("nmap_results.txt", 'w') as fw:   # 打开文件进行写操作
        for line in results:
            if line:
                fw.write(line + '\n')   # 写入每一行结果

def main():
    # 主函数：执行扫描和结果保存流程
    run_masscan()   # 运行masscan扫描
    task_list = extract_masscan()   # 提取扫描结果为任务列表
    if task_list:
        results = run_nmap(task_list)   # 使用nmap进一步扫描
        save_results(results)   # 保存最终结果

if __name__ == '__main__':
    main()  # 如果是直接运行此脚本，则执行main函数
