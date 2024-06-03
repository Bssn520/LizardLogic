import os
from datetime import datetime, timedelta
import re
import json
import requests
import warnings
import zipfile
from requests.exceptions import SSLError
import time


def open_folder(folder_path):
    # 检查文件夹是否存在
    if os.path.exists(folder_path):
        # 调用文件管理器打开文件夹
        os.startfile(folder_path)
    else:
        print(f"文件夹不存在: {folder_path}")


def download(url, max_retries=5, delay=2):
    # print(f"DEBUG:{url}")
    warnings.filterwarnings("ignore", message=".*SSL.*")
    for attempt in range(max_retries):
        try:
            # 发送HTTP请求
            response = requests.get(url, verify=False)
            # 如果请求成功，返回响应
            return response
        except SSLError as e:
            # 如果遇到SSLError异常，打印错误信息
            print(f"从GitHub下载必须文件失败: {e}")
            print(f"{delay} 秒后重新下载")
            # 等待一段时间后重试
            time.sleep(delay)
    # 如果重试次数用完，仍然失败，抛出异常
    raise Exception(f"尝试下载{max_retries}次仍然失败，请检查网络是否能正常访问 GitHub")


def download_applist(file_path):
    url = f"https://raw.githubusercontent.com/BlankTMing/ManifestAutoUpdate/001000001000/applist.json"
    r = download(url)
    with open(file_path, "wb") as f:
        f.write(r.content)


def check_update_applist(file_path):
    if not os.path.exists(file_path):
        return False
    # 获取文件的修改时间
    file_modified_time = os.path.getmtime(file_path)
    # 将时间戳转换为datetime对象
    file_modified_datetime = datetime.fromtimestamp(file_modified_time)
    # 获取当前时间
    current_time = datetime.now()
    # 计算时间差
    time_difference = current_time - file_modified_datetime

    # 如果文件超过一天未更新，则调用download函数重新下载
    if time_difference > timedelta(days=1):
        return False
    else:
        return True


def download_github_directory(appid):
    url = f"https://github.com/BlankTMing/ManifestAutoUpdate/archive/refs/heads/{appid}.zip"
    Key_url = f"https://github.com/hansaes/ManifestAutoUpdate/raw/{appid}/config.vdf"

    r = download(url)
    key = download(Key_url)
    with open(f"config.vdf", "wb") as f:
        f.write(key.content)

    with open(f"{appid}.zip", "wb") as f:
        f.write(r.content)
        with zipfile.ZipFile(f"{appid}.zip", "r") as zip_ref:
            zip_ref.extractall()


def read_vdf(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        return file.read()


def read_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        json_info_content = file.read()
        return json.loads(json_info_content)


def parse_vdf_to_lua(vdf_key_content, json_info_content):
    depot_key_pattern = r'"(\d+)"\s*{\s*"DecryptionKey"\s*"([0-9a-fA-F]+)"\s*}'
    depots = re.findall(depot_key_pattern, vdf_key_content)

    lua_lines = []

    appid = json_info_content.get("appId")
    if appid is not None:
        lua_lines.append(f"addappid({appid})")

    dlcs = json_info_content.get("dlcs")
    if dlcs is not None:
        for dlc_id in dlcs:
            lua_lines.append(f"addappid({dlc_id})")

    for depot_id, decryption_key in depots:
        lua_lines.append(f'addappid({depot_id},1,"{decryption_key}")')

        manifest_files = [
            f
            for f in os.listdir(f"ManifestAutoUpdate-{appid}/")
            if f.startswith(depot_id + "_") and f.endswith(".manifest")
        ]
        for manifest_file in manifest_files:
            manifest_id = manifest_file[len(depot_id) + 1 : -len(".manifest")]
            lua_lines.append(f'setManifestid({depot_id},"{manifest_id}",0)')

    return "\n".join(lua_lines)


def main():
    print("检查游戏列表更新并测试网络连接...")
    if not check_update_applist(f"applist.json"):
        print("更新游戏列表")
        download_applist(f"applist.json")
    applist = read_json(f"applist.json")

    print("appid 是 steam 游戏的唯一 ID，可前往")
    print("https://steamdb.info 搜索获取")
    appid = input("请输入要下载游戏的 appid：")

    try:
        appname = applist[appid][0]
    except KeyError:
        print(f"没有找到 appid {appid} 的游戏，上游暂未分享该游戏的解锁文件")
        return
    appfile_name = f"{appid}_{appname}"
    print(f"尝试下载 {appname} 解锁文件到当前文件夹下")

    download_github_directory(appid)
    vdf_key_content = read_vdf(f"config.vdf")
    json_info_content = read_json(f"ManifestAutoUpdate-{appid}/config.json")

    lua_script = parse_vdf_to_lua(vdf_key_content, json_info_content)

    # print("Lua 生成完成")

    os.remove(f"{appid}.zip")
    os.remove(f"config.vdf")
    os.remove(f"ManifestAutoUpdate-{appid}/Key.vdf")
    os.remove(f"ManifestAutoUpdate-{appid}/appinfo.vdf")
    os.remove(f"ManifestAutoUpdate-{appid}/config.json")
    os.rename(f"ManifestAutoUpdate-{appid}", f"{appfile_name}")

    with open(f"{appfile_name}/{appfile_name}.lua", "w") as lua_file:
        lua_file.write(lua_script)

    print(f"生成 {appname} 解锁文件成功")
    print(f"将 {appfile_name} 文件夹内所有文件拖动到 steamtools 的悬浮窗上")
    print(f"并按提示关闭 steam 后重新打开即可下载游玩 {appname}")
    print(f"即将弹出{appfile_name} 文件夹")
    open_folder(appfile_name)


if __name__ == "__main__":
    main()
