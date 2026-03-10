import os
import subprocess
import logging

# 取得 main.py 所在的資料夾
log_dir = os.path.dirname(os.path.realpath(__file__))
log_file = os.path.join(log_dir, "samba_manager.log")

# 設定日誌系統
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.StreamHandler()]
)

def check_root_permission():
    if os.geteuid() != 0:
        logging.warning("錯誤權限執行腳本！")
        print("請以 sudo 或 root 權限執行此腳本！")

def check_samba_installed():
    result = subprocess.run(['which', 'smbd'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

def install_samba_service():
    #only print message suggest
    print("我還沒寫安裝 Samba 服務的功能，但你可以使用以下命令來安裝 Samba 服務：")
    print("sudo apt-get update(debian/ubuntu) 或 sudo yum update(centos/rhel) 或 sudo pacman -Syu(arch)")
    print("sudo apt-get install samba -y(debian/ubuntu) 或 sudo yum install samba -y(centos/rhel) 或 sudo pacman -S samba(arch)")
    print("安裝完成後，請重新啟動此程式以繼續使用 Samba 管理功能。")

def read_samba_config():
    samba_config_path = '/etc/samba/smb.conf'
    if not os.path.exists(samba_config_path):
        return None

    shares = {}
    with open(samba_config_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('[') and 'global' not in line.lower():
                section = line.strip('[]\n')
                shares[section] = None
            elif line.strip().startswith('path =') and section:
                shares[section] = line.strip().split('=', 1)[1].strip()
    return shares if shares else None

def display_shared_folders():
    shares = read_samba_config()
    if shares:
        print("當前共享資料夾：")
        for name, path in shares.items():
            print(f"名稱: {name}, 路徑: {path}")
    else:
        print("尚未設定任何共享資料夾。")

def add_shared_folder():
    samba_config_path = '/etc/samba/smb.conf'
    section_template = """
[{name}]
   path = {path}
   read only = no
   browsable = yes
"""

    print("新增共享資料夾 (輸入 'q' 可取消)")
    folder_name = input("請輸入新的共享資料夾名稱：").strip()
    if folder_name.lower() == 'q':
        print("操作已取消。")
        return

    folder_path = input("請輸入共享資料夾的完整路徑：").strip()
    if folder_path.lower() == 'q':
        print("操作已取消。")
        return

    if not folder_name or not folder_path:
        print("名稱或路徑不能為空！")
        return

    # 確認路徑是否存在，若不存在則自動建立
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            logging.info(f"成功建立資料夾：{folder_path}")
            print(f"成功建立資料夾：{folder_path}")
        except Exception as e:
            logging.info(f"建立資料夾失敗：{e}")
            print(f"建立資料夾失敗：{e}")
            return

    # 檢查 Samba 設定檔是否存在
    if not os.path.exists(samba_config_path):
        logging.info(f"找不到 Samba 設定檔：{samba_config_path}")
        print(f"找不到 Samba 設定檔：{samba_config_path}")
        return

    # 將新設定寫入設定檔
    try:
        with open(samba_config_path, 'a') as config_file:
            config_file.write(section_template.format(name=folder_name, path=folder_path))
        logging.info(f"成功新增共享資料夾：{folder_name}")
        print(f"成功新增共享資料夾：{folder_name}")
    except Exception as e:
        logging.info(f"寫入設定檔失敗：{e}")
        print(f"寫入設定檔失敗：{e}")
        return

    # 重啟 smbd 服務
    subprocess.run(['systemctl', 'restart', 'smbd'], check=False)
    logging.info("Samba 服務已重新啟動，設定已生效！")
    print("Samba 服務已重新啟動，設定已生效！")

def delete_shared_folder():
    samba_config_path = '/etc/samba/smb.conf'

    print("刪除共享資料夾 (輸入 'q' 可取消)")
    folder_name = input("請輸入要刪除的共享資料夾名稱：").strip()
    if folder_name.lower() == 'q':
        print("操作已取消。")
        return

    if not folder_name:
        print("名稱不能為空！")
        return

    # 讀取設定檔內容
    try:
        with open(samba_config_path, 'r') as config_file:
            lines = config_file.readlines()

        # 尋找並刪除對應的段
        in_section = False
        new_lines = []
        for line in lines:
            if line.startswith(f'[{folder_name}]'):
                in_section = True
            elif in_section and line.strip() == "":
                in_section = False  # 離開該段
                continue
            elif not in_section:
                new_lines.append(line)

        # 檢查是否找到了目標設定
        if len(lines) == len(new_lines):
            print(f"未找到名為 '{folder_name}' 的共享資料夾設定！")
            return

        # 回寫檔案
        with open(samba_config_path, 'w') as config_file:
            config_file.writelines(new_lines)
        logging.info(f"成功刪除共享資料夾設定：{folder_name}")
        print(f"成功刪除共享資料夾設定：{folder_name}")
    except Exception as e:
        logging.info(f"修改設定檔失敗：{e}")
        print(f"修改設定檔失敗：{e}")
        return

    # 重啟 smbd 服務
    subprocess.run(['systemctl', 'restart', 'smbd'], check=False)
    logging.info("Samba 服務已重新啟動，設定已更新！")
    print("Samba 服務已重新啟動，設定已更新！")

def start_samba_service():
    confirm = input("確定要啟動 Samba 服務嗎？(y/n): ").strip().lower()
    if confirm == 'y':
        try:
            subprocess.run(['systemctl', 'start', 'smbd'], check=True)
            logging.info("Samba 服務已啟動！")
            print("Samba 服務已啟動！")
        except subprocess.CalledProcessError as e:
            logging.error(f"啟動服務失敗：{e}")
            print(f"啟動服務失敗：{e}")
    else:
        print("操作已取消。")

def stop_samba_service():
    confirm = input("確定要停止 Samba 服務嗎？(y/n): ").strip().lower()
    if confirm == 'y':
        try:
            subprocess.run(['systemctl', 'stop', 'smbd'], check=True)
            logging.info("Samba 服務已停止！")
            print("Samba 服務已停止！")
        except subprocess.CalledProcessError as e:
            logging.info(f"停止服務失敗：{e}")
            print(f"停止服務失敗：{e}")
    else:
        print("操作已取消。")

def check_samba_status():
    try:
        result = subprocess.run(['systemctl', 'is-active', 'smbd'], check=True, capture_output=True, text=True)
        status = result.stdout.strip()
        
        if status == "active":
            print("Samba 服務目前正在運行中。")
            return True
        else:
            print("Samba 服務未啟動，當前狀態：", status)
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"無法檢查 Samba 服務狀態：{e}")
        return False

def view_samba_log(last_n_lines = 10):
    log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "samba_manager.log")
    
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()  # 讀取所有行
            # 顯示最後 last_n_lines 行
            for line in lines[-last_n_lines:]:
                print(line.strip())
    except FileNotFoundError:
        print("日誌檔案未找到！")
