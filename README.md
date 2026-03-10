# Linux SMB Manager

用 Python 在 Linux 上透過命令列管理 Samba 服務，支援：

- 顯示目前共享資料夾
- 新增共享資料夾
- 刪除共享資料夾
- 啟動/停止 Samba 服務
- 查看程式日誌

## 環境需求

- Linux（使用 `systemctl`）
- Python 3
- Samba（`smbd`）
- `sudo` / root 權限

## 安裝

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3 samba
```

### Arch Linux

```bash
sudo pacman -Syu
sudo pacman -S samba
```

### CentOS / RHEL

```bash
sudo yum update -y
sudo yum install -y samba
```

## 使用方式

在專案根目錄執行：

```bash
sudo python3 main.py
```

啟動後會先檢查是否已安裝 `smbd`，接著進入互動式選單。

## 選單功能

```text
1. 顯示當前共享資料夾
2. 新增共享資料夾
3. 刪除共享資料夾
4. 啟動/停止 Samba 服務
5. 查看錯誤日誌
0. 離開
```

## 日誌位置

日誌檔會寫在：

- `my_package/samba_manager.log`

## 注意事項

- 程式會直接修改 `/etc/samba/smb.conf`，請確認你了解目前 Samba 設定。
- 新增或刪除共享後，程式會嘗試重啟 `smbd` 套用設定。
- 目前「安裝 Samba」功能為提示指令，不會自動安裝套件。

## License

本專案採用 MIT License，詳見 `LICENSE`。
