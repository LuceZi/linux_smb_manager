import os
import subprocess
import time

from my_package import samba_control

def clear_screen():
    #os.system('cls' if os.name == 'nt' else 'clear')
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

def echo_help():
    print("=== Samba 管理工具 ===")
    print("1. 顯示當前共享資料夾")
    print("2. 新增共享資料夾")
    print("3. 刪除共享資料夾")
    print("4. 啟動/停止 Samba 服務")
    print("5. 查看錯誤日誌")
    print("0. 離開")


def main():
    clear_screen()
    if samba_control.check_samba_installed():
        print("\nSamba 已安裝！")
    else:
        print("Samba 未安裝！，是否需要安裝服務")
        choice = input("是否需要安裝服務(y/n): ").strip()
        if choice == "y":
            samba_control.install_samba_service()
        else:
            return
    time.sleep(0.5)
    smb_status = samba_control.check_samba_status()
    while True:
        echo_help()
        choice = input("請選擇操作: ").strip().lower()

        if choice == "1":
            clear_screen()
            samba_control.display_shared_folders()
        elif choice == "2":
            clear_screen()
            samba_control.add_shared_folder()
        elif choice == "3":
            clear_screen()
            samba_control.display_shared_folders()
            samba_control.delete_shared_folder()
        elif choice == "4":
            clear_screen()
            if smb_status:
                print("停止 Samba 服務中...")
                samba_control.stop_samba_service()
            else:
                print("啟動 Samba 服務中...")
                samba_control.start_samba_service()
            smb_status = samba_control.check_samba_status()
            time.sleep(1)  # 暫停1秒來確認狀態更新
        elif choice == "5":
            clear_screen()
            samba_control.view_samba_log()
        elif choice == "0":
            exit_choice = input("確定要離開嗎？ (y/n): ").strip().lower()
            if exit_choice == 'y':
                print("離開程式")
                break
            else:
                print("繼續操作...")
        else:
            print("無效選項，請重新選擇！")
            time.sleep(2)
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"QAQ: {e}")
    finally:
        print("byee~~")



#====================wasted code====================
def main_old():
    if samba_control.check_samba_installed():
        print("\nSamba 已安裝！")
    else:
        print("Samba 未安裝！，是否需要安裝服務")
        choice = input("是否需要安裝服務(y/n): ").strip()
        if choice == "y":
            samba_control.install_samba_service()
        else:
            return
    
    time.sleep(0.5)
    smb_status = samba_control.check_samba_status()
    while True:
        print("\n=== Samba 管理選單 ===")
        print("1. 顯示當前共享資料夾")
        print("2. 新增共享資料夾")
        print("3. 刪除共享資料夾")
        if smb_status:
            print("4. 停止 Samba 服務")
        else:
            print("4. 啟動 Samba 服務")
        print("5. 查看錯誤日誌")
        print("0. 離開")
        choice = input("請選擇操作: ").strip().lower()

        if choice == "1":
            clear_screen()
            samba_control.display_shared_folders()
        elif choice == "2":
            clear_screen()
            samba_control.add_shared_folder()
        elif choice == "3":
            clear_screen()
            samba_control.display_shared_folders()
            samba_control.delete_shared_folder()
        elif choice == "4":
            clear_screen()
            if smb_status:
                print("停止 Samba 服務中...")
                samba_control.stop_samba_service()
            else:
                print("啟動 Samba 服務中...")
                samba_control.start_samba_service()
            smb_status = samba_control.check_samba_status()
            time.sleep(1)  # 暫停1秒來確認狀態更新
        elif choice == "5":
            clear_screen()
            samba_control.view_log()
        elif choice == "0":
            exit_choice = input("確定要離開嗎？ (y/n): ").strip().lower()
            if exit_choice == 'y':
                print("離開程式")
                break
            else:
                print("繼續操作...")
        else:
            print("無效選項，請重新選擇！")
            time.sleep(2)