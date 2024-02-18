from pathlib import Path
import shutil

# 定义work目录和qx目录的Path对象
rules_directory = Path('Rules')
qx_directory = rules_directory / 'QX'

# 同步work目录下的.list文件到qx目录中
for list_file in rules_directory.glob('*.list'):
    qx_file_path = qx_directory / list_file.name
    # 判断是否进行增量同步，即只有当qx目录中的文件不存在或者有更新时才复制
    if not qx_file_path.exists() or list_file.stat().st_mtime > qx_file_path.stat().st_mtime:
        shutil.copy(list_file, qx_file_path)
        print(f'文件 {list_file.name} 已同步到qx目录。')

# 在qx目录下执行脚本来更改.list文件
# 遍历qx目录下的所有.list文件
for file_path in qx_directory.glob('*.list'):
    # 读取文件内容
    with file_path.open('r', encoding='utf-8') as file:
        lines = file.readlines()

    # 确保文件不是空的
    if lines:
        # 获取文件第一行的字符串，忽略开头的#和空格
        fixed_string = lines[0].strip()[1:].strip()

        # 检查每一行并添加固定字符串（如果需要）
        with file_path.open('w', encoding='utf-8') as file:
            for i, line in enumerate(lines):
                # 如果行以#开头，或者是第一行，或者是空行，直接写入文件
                if line.strip().startswith('#') or i == 0 or not line.strip():
                    file.write(line)
                else:
                    # 检查行尾是否已经有固定字符串
                    if not line.strip().endswith(fixed_string):
                        # 如果没有，添加固定字符串
                        line = line.rstrip() + fixed_string + '\n'
                    file.write(line)

        print(f'文件 {file_path.name} 已被更新。')
    else:
        print(f'文件 {file_path.name} 是空的，没有进行更新。')
