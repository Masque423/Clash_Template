from pathlib import Path
import shutil

# 脚本所在目录的绝对路径
script_directory = Path(__file__).resolve().parent

# Rules 目录的绝对路径
rules_directory = script_directory.parent

# qx 目录的绝对路径
qx_directory = script_directory

# 用于跟踪是否有文件被更新
any_file_updated = False

# 同步 Rules 目录下的 .list 文件到 qx 目录中
for list_file in rules_directory.glob('*.list'):
    qx_file_path = qx_directory / list_file.name
    # 判断是否进行增量同步，即只有当 qx 目录中的文件不存在或者有更新时才复制
    if not qx_file_path.exists() or list_file.stat().st_mtime > qx_file_path.stat().st_mtime:
        shutil.copy(list_file, qx_file_path)
        print(f'文件 {list_file.name} 已同步到 QX 目录')
        any_file_updated = True

# 在 qx 目录下执行脚本来更改.list文件
# 遍历 qx 目录下的所有.list文件
for file_path in qx_directory.glob('*.list'):
    # 读取文件内容
    with file_path.open('r', encoding='utf-8') as file:
        lines = file.readlines()

    # 确保文件不是空的，并且有内容需要更新
    if lines:
        # 获取文件第一行的字符串，忽略开头的 # 和空格
        fixed_string = lines[0].strip()[1:].strip()
        updated = False  # 标记文件是否被更新

        # 准备更新后的内容
        new_lines = []
        for i, line in enumerate(lines):
            # 如果行以 # 开头，或者是第一行，或者是空行，直接写入文件
            if line.strip().startswith('#') or i == 0 or not line.strip():
                new_lines.append(line)
            else:
                # 检查行尾是否已经有固定字符串
                if not line.strip().endswith(fixed_string):
                    # 如果没有，添加固定字符串
                    line = line.rstrip() + fixed_string + '\n'
                    updated = True  # 标记为已更新
                new_lines.append(line)

        if updated:
            with file_path.open('w', encoding='utf-8') as file:
                file.writelines(new_lines)
            print(f'文件 {file_path.name} 已被更新')
            any_file_updated = True
            
# 如果没有文件被更新，则输出相应的内容
if not any_file_updated:
    print("已完成同步。")
