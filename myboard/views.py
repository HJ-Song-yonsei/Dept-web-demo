# myboard/views.py

from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    abort,
    current_app
)
from .models import fetch_board_items, db, Post
from . import myboard_bp
import os

# --- Freeze 플래그: 모듈 로드시에는 환경변수만 확인 ---
IS_FREEZING = os.getenv('IS_FREEZING') == '1'

# 비-freeze 환경에서만 확장자 없는 JSON 엔드포인트 등록
if not IS_FREEZING:
    @myboard_bp.route('/api/board')
    def board_api():
        items = fetch_board_items()
        return jsonify(items)

# 확장자 포함 JSON 엔드포인트 (freeze/비-freeze 모두에서 사용)
@myboard_bp.route('/api/board.json')
def board_api_json():
    items = fetch_board_items()
    return jsonify(items)

@myboard_bp.route('/board/<int:item_id>/')
def board_view(item_id):
    """화면 전체 전환 방식의 상세 보기"""
    items = fetch_board_items()
    # id로 매칭된 아이템 찾기
    item = next((i for i in items if i.get('id') == item_id), None)
    if not item:
        abort(404)

    # 이전/다음 아이템 탐색
    idx = items.index(item)
    prev_item = items[idx - 1] if idx > 0 else None
    next_item = items[idx + 1] if idx < len(items) - 1 else None

    return render_template(
        'board_detail.html',
        item=item,
        prev_item=prev_item,
        next_item=next_item
    )

# --- 정적 빌드가 아닐 때만 /posts/new 라우트 활성화 ---
if not IS_FREEZING:
    @myboard_bp.route(
        '/posts/new',
        endpoint='edit',
        methods=['GET', 'POST']
    )
    def new_post():
        """새 글 작성 폼 및 저장 처리"""
        if request.method == 'POST':
            # 1) 폼 데이터 추출
            notice  = request.form.get('notice', '')
            title   = request.form['title']
            author  = request.form.get('author', '')
            date    = request.form.get('date', '')
            content = request.form.get('content', '')

            # 2) DB에 저장
            post = Post(
                notice=notice,
                title=title,
                author=author,
                date=date,
                content=content
            )
            db.session.add(post)
            db.session.commit()

            # 3) 저장 후 목록 페이지(또는 /api/board)로 리다이렉트
            return redirect(url_for('myboard.board_api'))

        # GET 요청 시 작성 폼 렌더링
        return render_template('new_post.html')
