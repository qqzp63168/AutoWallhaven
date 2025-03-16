import datetime
import os
import shutil
import requests
from datetime import datetime

#==============================参数配置start============================================
# 定义文件夹路径
base_folder = "C:\\wallhaven"  # 基础文件夹,壁纸存放路径
page_count = 1 # 获取的页数，每页24张
# 请求参数 api参考文档https://wallhaven.cc/help/api
query_params = {
    # "apikey": "", # 你的 API Key
    "sorting": "toplist",
    "topRange": "1M",
    "purity": "111",
    "page": "1"
}
#==============================参数配置end==============================================

source_folder = f"{base_folder}\\current"  # 源文件夹
backup_base_folder = f"{base_folder}\\backup"  # 备份文件夹
# 请求地址
search_url = "https://wallhaven.cc/api/v1/search"
# 图片URL列表
image_urls = []
# 获取当前时间并格式化为字符串
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_folder = f"{backup_base_folder}\\{current_time}"  # 备份文件夹

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
def download_new_images(image_urls):
    os.makedirs(source_folder, exist_ok=True)  # 确保源文件夹存在
    for index, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # 使用 os.path.basename 获取文件名
                filename = os.path.basename(url)
                save_path = os.path.join(source_folder, filename)
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"已下载: {filename}")
            else:
                print(f"下载失败: {url}，状态码: {response.status_code}")
        except Exception as e:
            print(f"下载 {url} 时出错: {e}")
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