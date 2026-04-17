import datetime
import os
import shutil
import sys
import requests
from datetime import datetime
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

#==============================参数配置start============================================
# 定义文件夹路径
base_folder = "D:\\System\\pic\\壁纸\\wallhaven"  # 基础文件夹,壁纸存放路径
page_count = 2 # 获取的页数，每页24张
download_threads = 8  # 并发下载线程数，建议4-16
# 请求参数 api参考文档https://wallhaven.cc/help/api
query_params = {
    "apikey": "", # 你的 API Key
    "sorting": "toplist",
    "topRange": "1w",
    "purity": "111",
    "ratios": "landscape",
    "atleast": "3840x2160",
    "page": "1"
}
#==============================参数配置end==============================================
source_folder = f"{base_folder}\\current"  # 源文件夹
backup_base_folder = f"{base_folder}\\backup"  # 备份文件夹
os.makedirs(base_folder, exist_ok=True)  # 确保基础文件夹存在
os.makedirs(source_folder, exist_ok=True)  # 确保源文件夹存在
# 请求地址
search_url = "https://wallhaven.cc/api/v1/search"
# 图片URL列表
image_urls = []
# 获取当前时间并格式化为字符串
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_folder = f"{backup_base_folder}\{current_time}"  # 备份文件夹

# 检查 Clash Verge 是否运行并启动
clash_path = "D:\\Program Files\\Clash Verge\\clash-verge.exe"
def check_and_start_clash():
    # 检查 Clash Verge 是否正在运行
    try:
        # 使用 tasklist 命令检查进程
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq clash-verge.exe"],
            capture_output=True,
            text=True
        )
        # 检查输出中是否包含 clash-verge.exe
        if "clash-verge.exe" in result.stdout:
            print("Clash Verge 已经在运行中")
        else:
            print("Clash Verge 未运行，正在启动...")
            # 启动 Clash Verge
            subprocess.Popen([clash_path])
            print("Clash Verge 已启动，等待1分钟...")
            # 等待1分钟
            time.sleep(60)
            print("等待完成，继续执行")
    except Exception as e:
        print(f"检查或启动 Clash Verge 时出错: {e}")

# 复制图片到备份文件夹
def backup_images():
    # 获取目录内容
    folder_contents = os.listdir(source_folder)

    # 判断目录内容列表的长度是否为 0
    if len(folder_contents) == 0:
        print("目录为空")
        return
    # 创建备份文件夹
    os.makedirs(backup_folder, exist_ok=True)
    for filename in folder_contents:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp','webp')):
            src_path = os.path.join(source_folder, filename)
            dst_path = os.path.join(backup_folder, filename)
            shutil.move(src_path, dst_path)
            print(f"已备份: {filename}")

# 下载新的图片到源文件夹
def download_single_image(url):
    try:
        session = requests.Session()
        response = session.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            filename = os.path.basename(url)
            save_path = os.path.join(source_folder, filename)
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            return f"已下载: {filename}"
        else:
            return f"下载失败: {url}，状态码: {response.status_code}"
    except Exception as e:
        return f"下载 {url} 时出错: {e}"

def download_new_images(image_urls):
    os.makedirs(source_folder, exist_ok=True)
    print(f"开始下载，共 {len(image_urls)} 张图片，使用 {download_threads} 个线程...")
    
    with ThreadPoolExecutor(max_workers=download_threads) as executor:
        futures = {executor.submit(download_single_image, url): url for url in image_urls}
        for future in as_completed(futures):
            result = future.result()
            print(result)
    
    print("下载完成!")
# 获取图片URL列表
def get_image_urls():
    # 发送请求
    response = requests.get(search_url,query_params)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析返回的 JSON 数据
        data = response.json()
        # 遍历 data 数组
        for item in data['data']:
            # 获取每个元素的 id
            item_id = item['id']
            print(f"Item ID: {item_id}")

            # 获取每个元素的 url
            item_url = item['url']
            print(f"Item URL: {item_url}")

            # 获取每个元素的 path
            item_pth = item['path']
            print(f"Item Path: {item_pth}")
            image_urls.append(item_pth)
            print("----------------------")
    else:
        print(f"请求失败，状态码：{response.status_code}")



# 执行备份和下载
if __name__ == "__main__":
    print("开始检查 Clash Verge 是否运行...")
    check_and_start_clash()
    print("开始备份图片...")
    backup_images()
    print("备份完成，开始获取图片URL...")
    for i in range(page_count):
        query_params['page'] = i + 1
        print(f"正在获取第 {i + 1} 页的图片URL...")
        get_image_urls()
    print("url获取完成，开始下载新图片...")
    download_new_images(image_urls)
    print("所有操作完成")
    sys.exit(0)