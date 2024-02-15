# 读取 mmdb 数据库
from pathlib import Path
import maxminddb

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

def open_mmdb_file(mmdb_file_path, ip_address):
    reader = maxminddb.open_database(mmdb_file_path)
    result = reader.get(ip_address)
    reader.close()
    return result

result = open_mmdb_file(mmdb_file_path, ip_address)
print(result)