import paramiko
from dotenv import load_dotenv
import os


# read .env
load_dotenv()


hostname = os.getenv('MAIA_HOSTNAME')
username = os.getenv('MAIA_USERNAME')
password = os.getenv('MAIA_PASSWORD')
port = os.getenv('MAIA_PORT')


def send_files_via_ssh(
    hostname: str,
    port: int,
    username: str,
    password: str,
    *file_paths: tuple[str, str]  # 可変長引数：各タプルは (local_path, remote_path)
):
    try:
        
        

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)

        sftp = ssh.open_sftp()

        for local_path, remote_path in file_paths:
            print(f"📤 送信中: {local_path} → {remote_path}")
            sftp.put(local_path, remote_path)

        sftp.close()
        ssh.close()
        print("✅ すべてのファイルを送信しました。")

    except Exception as e:
        print(f"❌ エラー: {e}")

# 使用例
if __name__ == "__main__":

    

    send_files_via_ssh(
        hostname,
        port,
        username,
        password,
        ("./data/wrf_conf/namelist.input", f"/home/{username}/WRF/backup/namelist.input"),
        ("./data/wrf_conf/namelist.wps", f"/home/{username}/WRF/backup/namelist.wps"),
        
    )
