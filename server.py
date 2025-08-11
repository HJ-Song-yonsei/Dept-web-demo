# server.py

import os
import sys
from dotenv import load_dotenv
from flask import Flask, send_from_directory, abort, render_template, jsonify

# 1) 프로젝트 루트를 모듈 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 2) .env 로드
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# ★ Freeze 플래그 반영
if os.getenv('IS_FREEZING') == '1':
    app.config['IS_FREEZING'] = True
IS_FREEZING = app.config.get('IS_FREEZING', False)

# ★ SQLAlchemy 기본값 (freeze 시 메모리 SQLite)
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
if 'SQLALCHEMY_DATABASE_URI' not in app.config:
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///:memory:' if IS_FREEZING else 'sqlite:///app.db'
    )

# ★ 템플릿에서 IS_FREEZING 사용 가능하도록 주입
@app.context_processor
def inject_flags():
    return dict(IS_FREEZING=IS_FREEZING)

# DB/블루프린트 등록
from myboard import myboard_bp
from myboard.models import db
db.init_app(app)
app.register_blueprint(myboard_bp)

# 설정 로드
try:
    app.config.from_object('config.Config')
except Exception:
    pass    

# 라우트 예시
@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

# @app.route('/js/<path:filename>')
# def serve_js(filename):
#     return send_from_directory('js', filename)

if not app.config['IS_FREEZING']:
    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory('.', path)

# 앱 실행
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
