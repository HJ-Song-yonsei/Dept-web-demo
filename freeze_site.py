# freeze_site.py
import os, shutil
from flask_frozen import Freezer

# ★ 서버 임포트 전에 Freeze 플래그 설정
os.environ['IS_FREEZING'] = '1'

from server import app  # server.py에서 Flask app 생성

# 앱 설정
app.config['IS_FREEZING'] = True
app.config.setdefault('FREEZER_RELATIVE_URLS', True)
app.config.setdefault('FREEZER_DESTINATION', os.path.join(os.path.dirname(__file__), 'build'))
app.config.setdefault('FREEZER_REMOVE_EXTRA_FILES', True)
app.config.setdefault('FREEZER_IGNORE_404_NOT_FOUND', True)

freezer = Freezer(app)

# /board/<int:item_id>/ 동결 (뷰 라우트도 슬래시 종결이어야 함)
@freezer.register_generator
def myboard_board_view():
    """myboard.board_view(endpoint)에 필요한 item_id들을 생성"""
    from myboard.models import fetch_board_items
    for it in fetch_board_items():
        yield 'myboard.board_view', {'item_id': int(it['id'])}

# /api/board.json 동결
@freezer.register_generator
def myboard_board_api_json():
    yield 'myboard.board_api_json', {}

if __name__ == '__main__':
    # 매 빌드 전 이전 산출물 제거 (디렉토리/파일 충돌 예방)
    build_dir = app.config['FREEZER_DESTINATION']
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # ★ board.js를 앱 정적 경로(./js/board.js)로 복사
    proj_root = os.path.dirname(__file__)
    src = os.path.join(proj_root, 'myboard', 'static', 'js', 'board.js')
    dst = os.path.join(proj_root, 'js', 'board.js')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(src):
        shutil.copy2(src, dst)

    freezer.freeze()
