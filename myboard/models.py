
import os
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    notice   = db.Column(db.String(50))
    title    = db.Column(db.String(200))
    author   = db.Column(db.String(100))
    date     = db.Column(db.String(50))
    content  = db.Column(db.Text)
    # files 등 추가 컬럼 정의…

def fetch_board_items():
    # 프로젝트 루트에서 data/posts.json 경로 계산
    base_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(base_dir, '..', 'data', 'posts.json')

    with open(path, encoding='utf-8') as f:
        items = json.load(f)

    # notice 먼저, 나머지는 ID 내림차순
    notices = [i for i in items if i.get('notice') == '공지']
    normals = sorted(
        [i for i in items if i.get('notice') != '공지'],
        key=lambda x: x['id'], reverse=True
    )
    return notices + normals