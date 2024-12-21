import requests
from flask import Flask, request, jsonify, redirect
import hashlib
import random
import datetime
from urllib.parse import urlparse, parse_qs
from cachetools import cached, TTLCache
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

def get_tarot_card(user_id):
    tarot_cards = ["愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人", "战车",
                  "力量", "隐士", "命运之轮", "正义", "倒吊人", "死亡", "节制", "恶魔",
                  "塔", "星星", "月亮", "太阳", "审判", "世界"]
    today = datetime.date.today().strftime("%Y-%m-%d")
    combined = user_id + today
    hash_value = int(hashlib.sha256(combined.encode()).hexdigest(), 16)
    index = hash_value % len(tarot_cards)
    return tarot_cards[index]

@cached(cache=TTLCache(maxsize=1, ttl=5))
def get_hitokoto():
    response = requests.get('https://v1.hitokoto.cn/')
    if response.status_code == 200:
        data = response.json()
        return data.get('hitokoto')
    else:
        return "获取一言失败"

@app.route('/api/handler', methods=['POST'])
def lark_api_handler():
    body = request.json
    if app.debug:
        print(body)

    # 回调验证
    if body and body.get('type') == 'url_verification':
        return jsonify({'challenge': body.get('challenge')})

    if body and body.get('header', {}).get('event_type') == 'url.preview.get':
        user_id = body.get('event', {}).get('operator', {}).get('open_id')
        if user_id:
            url = body.get('event', {}).get('context', {}).get('url')
            # 提取路径部分
            parsed_url = urlparse(url)
            path = parsed_url.path
            if path == '/time':
                inline_title = "当前时间是：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif path == '/tarot':
                tarot_card = get_tarot_card(user_id)
                inline_title = "今天你的塔罗牌是：" + tarot_card
            elif path == '/hitokoto':
                inline_title = get_hitokoto()
            elif path == '/weather':
                # 从 URL 的查询参数中获取 city 信息
                query_params = parse_qs(parsed_url.query)
                city = query_params.get('city', [None])[0]
                if city is None:
                    city = '110000'
                weather_info = query_weather(city)
                if weather_info:
                    inline_title = weather_info
                else:
                    inline_title = "获取天气失败"
            else:
                inline_title = "你好 Marscode"
            return jsonify({
                'inline': {
                    'i18n_title': {
                        'zh_cn': inline_title,
                    },
                    'image_key': 'img_v3_02gp_bc939d82-ad8d-4dd0-856d-c26e2d161b9g',
                },
            })
        else:
            return jsonify({'error': 'No user ID found'})

    return jsonify({})

@app.route('/time')
def time():
    return redirect('https://time.is/')

@app.route('/tarot')
def tarot():
    return redirect('https://tarotap.com/zh/card_meanings')

@app.route('/hitokoto')
def hitokoto_redirect():
    return redirect('https://hitokoto.cn/')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect('https://www.marscode.cn/')

def query_weather(city):
    # 假设高德天气 API 的 key 存储在环境变量中
    api_key = os.getenv('AMAP_WEATHER_API_KEY')
    # 构建请求 URL
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city={city}"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        # 假设提取天气信息的逻辑，根据高德天气 API 的实际响应结构调整
        city_name = weather_data.get('lives')[0].get('city')
        weather_info = weather_data.get('lives')[0].get('weather')
        # 构建新的返回格式
        result = f"【{city_name}】今天的天气：【{weather_info}】"
        return result
    else:
        return None
