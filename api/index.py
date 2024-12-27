from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/handler', methods=['POST'])
def handler():
    body = request.json
    if app.debug:
        print(body)

    # 回调验证
    if body and body.get('type') == 'url_verification':
        return jsonify({'challenge': body.get('challenge')})

    if body and body.get('header', {}).get('event_type') == 'url.preview.get':
        # 计算距离元旦的天数
        today = datetime.now()
        new_year = datetime(today.year + 1, 1, 1)
        days_until_new_year = (new_year - today).days

        return jsonify({
            'inline': {
                'i18n_title': {
                    'zh_cn': f'元旦还有{days_until_new_year}天',
                },
                'image_key': 'img_v3_02e1_cf42a888-b257-4f5a-9ad7-22317623e75g',
            },
        })

    return jsonify({})

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'