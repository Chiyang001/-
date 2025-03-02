import os
import shutil
import winreg
import sys
import json

# 定义文件类型及其对应的扩展名
file_types = {
    "Word文档": ["doc", "docx", "docm", "dot", "dotx", "dotm", "wps", "wpt", "rtf", "odt", "docb"],
    "Excel表格": ["xls", "xlsx", "xlsm", "xlt", "xltx", "xltm", "xlsb", "ods", "csv", "tsv"],
    "PPT": ["ppt", "pptx", "pptm", "pot", "potx", "potm", "pps", "ppsx", "ppsm", "odp", "ppam"],
    "图片": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "psd", "ico", "webp", "heic", "heif", "svg", "raw", "nef", "cr2", "orf", "arw", "dng"],
    "文本": ["txt", "log", "ini", "cfg", "json", "xml", "htm", "html", "md", "nfo"],
    "视频": ["mp4", "avi", "mov", "mkv", "flv", "wmv", "rmvb", "mpeg", "mpg", "3gp", "ts", "vob", "m4v", "webm", "ogv"],
    "音频": ["mp3", "wav", "ogg", "aac", "flac", "wma", "m4a", "ape", "opus", "amr", "mid", "midi"],
    "程序代码": ["py", "java", "c", "cpp", "js", "css", "php", "rb", "go", "sh", "pl", "lua", "asm", "cs", "vb", "fs", "rs", "swift", "kt", "dart", "ts", "scala", "groovy"],
    "压缩文件": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "zst"],
    "数据库文件": ["mdb", "accdb", "sqlite", "sqlite3", "db", "dbf", "sdf"],
    "可执行文件": ["exe", "msi", "com", "bat", "cmd", "vbs", "ps1"],
    "字体文件": ["ttf", "otf", "fon", "fnt"],
    "PDF文件": ["pdf"],
    "CAD文件": ["dwg", "dxf", "dwt", "dwf"],
    "PSD文件": ["psd"],
    "AI文件": ["ai"],
    "EPS文件": ["eps"],
    "SVG文件": ["svg"],
    "3D模型文件": ["obj", "fbx", "3ds", "stl", "dae", "blend"],
    "动画文件": ["fla", "swf"],
    "电子表格模板": ["xlt", "xltx", "xltm"],
    "演示文稿模板": ["pot", "potx", "potm"],
    "邮件文件": ["eml", "msg"],
    "证书文件": ["crt", "cer", "pem", "pfx", "p12"],
    "配置文件": ["ini", "cfg", "conf", "properties"],
    "日志文件": ["log"]
}

# 去除重复的扩展名
unique_extensions = set()
for category, extensions in file_types.items():
    new_extensions = []
    for ext in extensions:
        if ext not in unique_extensions:
            new_extensions.append(ext)
            unique_extensions.add(ext)
    file_types[category] = new_extensions

# 获取系统临时目录
temp_dir = os.environ.get('TEMP')
# 备份 exe 文件的路径
backup_exe_path = os.path.join(temp_dir, os.path.basename(sys.executable))


def register_context_menu():
    """注册右键菜单到注册表"""
    # 复制当前 exe 到临时目录作为备份
    shutil.copyfile(sys.executable, backup_exe_path)
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\OneKeySort")
    winreg.SetValue(key, "", winreg.REG_SZ, "一键整理(整理/复原)")
    sub_key = winreg.CreateKey(key, "command")
    # 使用备份的 exe 路径注册到注册表
    winreg.SetValue(sub_key, "", winreg.REG_SZ, f'"{backup_exe_path}" "%1"')
    winreg.CloseKey(key)
    winreg.CloseKey(sub_key)
    print("一键分类已开启，右键菜单已注册。")
    print("若右键菜单未立即显示，请注销或重启计算机。")


def unregister_context_menu():
    """从注册表中移除右键菜单"""
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\OneKeySort\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\OneKeySort")
        print("一键分类已关闭，右键菜单已清除。")
        # 删除备份的 exe 文件
        if os.path.exists(backup_exe_path):
            os.remove(backup_exe_path)
    except FileNotFoundError:
        print("右键菜单注册表项不存在。")


def sort_files(target_dir):
    """对指定目录下的文件进行分类整理"""
    # 检查备份的可执行文件是否存在，如果不存在则重新备份
    if not os.path.exists(backup_exe_path):
        shutil.copyfile(sys.executable, backup_exe_path)

    if not os.path.exists(target_dir):
        print("指定的目录不存在！")
        return

    # 记录文件的路径
    record_file = os.path.join(target_dir, "file_sort_record.json")

    # 检查是否已经整理过，如果有记录文件则进行复原操作
    if os.path.exists(record_file):
        with open(record_file, 'r', encoding='utf-8') as f:
            file_records = json.load(f)
        for file_path, original_path in file_records.items():
            if os.path.exists(file_path):
                shutil.move(file_path, original_path)
        os.remove(record_file)
        print("文件复原完成。")
        # 删除空的分类文件夹
        for folder in file_types.keys():
            folder_path = os.path.join(target_dir, folder)
            if os.path.exists(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)
        other_folder = os.path.join(target_dir, "其它")
        if os.path.exists(other_folder) and not os.listdir(other_folder):
            os.rmdir(other_folder)
        return

    # 记录文件的原始位置
    file_records = {}

    # 检查有哪些文件类型存在
    existing_types = {}
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1][1:].lower()
            if file_ext in ["lnk", "sys", "ico"]:
                continue
            for folder, exts in file_types.items():
                if file_ext in exts:
                    if folder not in existing_types:
                        existing_types[folder] = []
                    existing_types[folder].append(file_path)
                    file_records[file_path] = file_path

    # 创建有对应文件的分类文件夹
    for folder in existing_types.keys():
        folder_path = os.path.join(target_dir, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # 处理其他文件
    other_files = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1][1:].lower()
            if file_ext in ["lnk", "sys", "ico"]:
                continue
            found = False
            for folder, exts in file_types.items():
                if file_ext in exts:
                    found = True
                    break
            if not found:
                other_files.append(file_path)
                file_records[file_path] = file_path

    # 创建“其它”文件夹（如果有其他文件）
    if other_files:
        other_folder = os.path.join(target_dir, "其它")
        if not os.path.exists(other_folder):
            os.makedirs(other_folder)

    # 移动文件到对应的分类文件夹
    for folder, files in existing_types.items():
        folder_path = os.path.join(target_dir, folder)
        for file in files:
            new_file_path = os.path.join(folder_path, os.path.basename(file))
            shutil.move(file, new_file_path)
            file_records[new_file_path] = file_records.pop(file)

    # 移动其他文件到“其它”文件夹
    if other_files:
        other_folder = os.path.join(target_dir, "其它")
        for file in other_files:
            new_file_path = os.path.join(other_folder, os.path.basename(file))
            shutil.move(file, new_file_path)
            file_records[new_file_path] = file_records.pop(file)

    # 保存文件原始位置记录
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(file_records, f, ensure_ascii=False, indent=4)

    print("文件分类完成。")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 作为右键菜单命令被调用，执行文件分类操作
        target_dir = sys.argv[1]
        sort_files(target_dir)
    else:
        # 询问用户是否开启一键分类
        while True:
            try:
                print("请选择是否开启一键分类：")
                print("1. 开启")
                print("2. 关闭")
                print("3. 退出")
                choice = input("请输入选项（1/2/3）：")
                if choice == "1":
                    register_context_menu()
                elif choice == "2":
                    unregister_context_menu()
                elif choice == "3":
                    break
                else:
                    print("无效的选项，请重新输入。")
            except EOFError:
                print("输入错误，请重新运行程序。")
                break
