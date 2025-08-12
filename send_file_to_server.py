import paramiko
from dotenv import load_dotenv
import os
from scp import SCPClient
from utils.tools import choice_folders, get_foldername


# read .env
load_dotenv()


hostname = os.getenv('MAIA_HOSTNAME')
username = os.getenv('MAIA_USERNAME')
password = os.getenv('MAIA_PASSWORD')
port = os.getenv('MAIA_PORT')


def upload_dir(
    hostname: str,
    port: int,
    username: str,
    password: str,
    folderpaths: tuple[str, str]
):
    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.load_system_host_keys()
            ssh.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password
            )

            from_folder, to_folder = folderpaths

            with SCPClient(ssh.get_transport()) as scp:
                scp.put(
                    remote_path=to_folder,
                    files=from_folder,
                    recursive=True # ディレクトリごとのときは、ここがTrue
                )
    except Exception as e:
        print(f"❌ エラー: {e}")

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
    print(get_foldername(path=['data/wrf_conf']))
    folderpath_list = choice_folders(get_foldername(path=['data/wrf_conf']))
    print(folderpath_list)
    foldername = os.path.basename(folderpath_list[0])
    upload_dir(
        hostname,
        port,
        username,
        password,
        (folderpath_list[0], f'/home/{username}/WRF/backup/{foldername}')
    )

    # send_files_via_ssh(
    #     hostname,
    #     port,
    #     username,
    #     password,
    #     ("./data/wrf_conf/namelist.input", f"/home/{username}/WRF/backup/namelist.input"),
    #     ("./data/wrf_conf/namelist.wps", f"/home/{username}/WRF/backup/namelist.wps"),
        
    # )
