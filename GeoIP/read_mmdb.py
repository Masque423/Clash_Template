# 读取 mmdb 数据库
import re
from pathlib import Path
import maxminddb
import socket

# 当前文件的路径
current_file = Path(__file__).resolve()

# 当前文件的目录
dir_path = current_file.parent

# 构建相对路径
# relative_path = dir_path / 'my_folder' / 'my_file.txt'
mmdb_file_path = dir_path / 'Country.mmdb'

# mmdb_file_path = 'D:\Code\Clash_Template\Country.mmdb'
# ip_address = '23.94.43.143'
# ip_address = '8.134.239.150'
ip_address = '167.114.153.81'

def get_ips(domain):
    try:
        # 获取域名对应的所有记录，包括 IPv4 和 IPv6 地址
        infos = socket.getaddrinfo(domain, None)
        ip_address = list(set(info[4][0] for info in infos))
        return ip_address
    except socket.gaierror as e:
        print(f"Error resolving domain {domain}: {e}")
        return None

def get_geo_info(mmdb_file_path, ip_address):
    reader = maxminddb.open_database(mmdb_file_path)
    result = reader.get(ip_address)
    reader.close()
    if result and 'country' in result:
        country_data = result['country']
        iso_code = country_data.get('iso_code','Unknown')
        country_name = country_data.get('names',{}).get('zh-CN','Unknown')
        return f"{iso_code}, {country_name}"
    else:
        return "No country infomation available."

def is_ip_address(input_str):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}&$")
    return pattern.match(input_str) is not None
    

def process_input(user_input):
    # 检查用户输入是否为 IP 地址
    if is_ip_address(user_input):
        # 如果是
        geo_info = get_geo_info(mmdb_file_path,user_input)
        print(geo_info)
    else:
        # 如果不是，假设是域名，获取 IP 地址列表
        ips = get_ips(user_input)
        if ips:
            print(f"IP address for domain {user_input}: {ips}")
            # 对每个 IP 地址，输出位置信息
            for ip in ips:
                geo_info = get_geo_info(mmdb_file_path, ip)
                print(geo_info)
        else:
            print("No IP address found for domain.")

user_input = input("Please enter an IP address or domain name: ")
process_input(user_input)

#result = get_geo_info(mmdb_file_path, ip_address)
#print(result)


""" mmdb 文件输出示例
{
    'continent': {
        'code': 'NA', 
        'geoname_id': 6255149, 
        'names': {
            'de': 'Nordamerika', 
            'en': 'North America', 
            'es': 'Norteamérica', 
            'fr': 'Amérique du Nord', 
            'ja': '北アメリカ', 
            'pt-BR': 'América do Norte', 
            'ru': 'Северная Америка', 
            'zh-CN': '北美洲'
        }
    }, 
    'country': {
        'geoname_id': 6251999, 
        'iso_code': 'CA', 
        'names': {
            'de': 'Kanada', 
            'en': 'Canada', 
            'es': 'Canadá', 
            'fr': 'Canada', 
            'ja': 'カナダ', 
            'pt-BR': 'Canadá', 
            'ru': 'Канада', 
            'zh-CN': '加拿大'
        }
    }, 
    'registered_country': {
        'geoname_id': 6251999, 
        'iso_code': 'CA', 
        'names': {
            'de': 'Kanada', 
            'en': 'Canada', 
            'es': 'Canadá', 
            'fr': 'Canada', 
            'ja': 'カナダ', 
            'pt-BR': 'Canadá', 
            'ru': 'Канада', 
            'zh-CN': '加拿大'
        }
    }
}
"""
