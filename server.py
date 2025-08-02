# server.py

import os
import sys
from dotenv import load_dotenv
from flask import Flask, send_from_directory, abort, render_template, jsonify
from myboard import myboard_bp
from myboard.models import db

# 1) 프로젝트 루트를 모듈 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 2) .env 로드
load_dotenv()

# 3) Flask 앱 생성 (static_folder='.' 로 루트 정적 파일 매핑)
app = Flask(__name__, static_folder='.', static_url_path='')

# 4) 설정 로드
app.config.from_object('config.Config')

# 5) SQLAlchemy 초기화
db.init_app(app)

# 6) Blueprint 등록
app.register_blueprint(myboard_bp)

# 7) 정적 파일 서빙 라우트
@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

# 8) 앱 실행
if __name__ == '__main__':
    # 앱 컨텍스트 안에서 DB 테이블 생성
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
