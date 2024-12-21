from flask import Flask, request, jsonify
import hashlib
import random
import datetime

app = Flask(__name__)

def get_tarot_card(user_id):
    tarot_cards = ["愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人", "战车",
                  "力量", "隐士", "命运之轮", "正义", "倒吊人", "死亡", "节制", "恶魔",
                  "塔", "星星", "月亮", "太阳", "审判", "世界"]
    today = datetime.date.today().strftime("%Y-%m-%d")
    combined = user_id + today
    hash_value = int(hashlib.sha256(combined.encode()).hexdigest(), 16)
    index = hash_value % len(tarot_cards)
    return tarot_cards[index]

@app.route('/api/handler', methods=['POST'])
def handler():
    body = request.json
    if app.debug:
        print(body)

    # 回调验证
    if body and body.get('type') == 'url_verification':
        return jsonify({'challenge': body.get('challenge')})

    if body and body.get('header', {}).get('event_type') == 'url.preview.get':
        user_id = body.get('event', {}).get('operator', {}).get('open_id')
        if user_id:
            tarot_card = get_tarot_card(user_id)
            return jsonify({
                'inline': {
                    'i18n_title': {
                        # 获取用户的塔罗牌并将其作为标题返回，添加前缀
                        'zh_cn': "今天你的塔罗牌是：" + tarot_card,
                    },
                    'image_key': 'img_v3_02gp_bc939d82-ad8d-4dd0-856d-c26e2d161b9g',
                },
            })
        else:
            return jsonify({'error': 'No user ID found'})

    return jsonify({})

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
