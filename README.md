# 介绍
自动从wallhaven.cc下载壁纸到指定目录，并且备份，可以自己定义配置

# 安装
在安装依赖之前，请确保你的系统中已安装 Python 和 pip。运行以下命令来安装项目所需的依赖：
```sh
pip install -r requirements.txt
```
# 运行
运行脚本以开始下载壁纸：
```sh
python wallpaper.py
```
# 配置（可选）
在运行脚本之前，请根据你的需求修改 wallpaper.py 文件开头部分的参数：
```python
#定义文件夹路径
base_folder = "C:\\wallhaven"  # 基础文件夹，壁纸存放路径
page_count = 1  # 获取的页数，每页24张

#请求参数，API 参考文档：https://wallhaven.cc/help/api
query_params = {
    # "apikey": "",  # 你的 API Key（可选）
    "sorting": "toplist",
    "topRange": "1M",
    "purity": "111",
    "page": "1"
}
```
注意：如果你需要使用 API Key，请前往 Wallhaven 官方文档 了解如何获取。
# 建议
将系统壁纸幻灯片的目录设置为配置中指定的基础文件夹（如 C:\\wallhaven）。 <br>
建议设置一个计划任务，每月自动运行此脚本以更新壁纸。