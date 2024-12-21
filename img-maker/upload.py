import requests, os
from dotenv import load_dotenv

load_dotenv()

# 飞书开放平台的API地址
FEISHU_API_URL = "https://open.feishu.cn/open-apis"

# 应用的App ID和App Secret
APP_ID = os.environ['FEISHU_APP_ID']
APP_SECRET = os.environ['FEISHU_APP_SECRET']

# 获取访问令牌
def get_access_token():
    url = f"{FEISHU_API_URL}/auth/v3/app_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    response = requests.post(url, json=payload)
    data = response.json()
    return data["app_access_token"]

# 上传图片
def upload_image(access_token, image_path):
    url = f"{FEISHU_API_URL}/image/v4/put/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    files = {
        "image": open(image_path, "rb"),
    }
    data = {
        "image_type": "message"
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    data = response.json()
    return data

# 使用示例
access_token = get_access_token()
image_path = "output.png"
upload_result = upload_image(access_token, image_path)
print(upload_result)