import streamlit as st
import json
import os
from datetime import datetime
import sys
from io import StringIO
import subprocess
import tempfile

st.set_page_config(page_title="PyShare", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }

    body, .stMarkdown {
        color: #1a1a1a !important;
        background-color: #fafafa !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #fafafa;
    }

    .stTextInput > label, .stTextArea > label {
        color: #1a1a1a !important;
        font-weight: 600;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        color: #1a1a1a !important;
        background-color: #fff !important;
        border: 2px solid #ff8c00 !important;
    }

    .stRadio > label, .stSelectbox > label {
        color: #1a1a1a !important;
        font-weight: 600;
    }

    .stButton > button {
        background: linear-gradient(135deg, #ff8c00 0%, #ff6600 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 20px !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 4px 12px rgba(255, 140, 0, 0.3) !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }

    .navbar {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 12px 24px;
        border-bottom: 3px solid #ff8c00;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -70px -24px 20px;
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .navbar-logo {
        font-size: 28px;
        font-weight: 700;
        color: #ff8c00;
        letter-spacing: -0.5px;
    }

    .navbar-user {
        color: white;
        font-size: 14px;
        font-weight: 500;
    }

    .choice-button {
        display: inline-block;
        padding: 20px 40px;
        margin: 10px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        cursor: pointer;
        border: 3px solid #ff8c00;
        background-color: white;
        color: #ff8c00;
        transition: all 0.3s;
        text-align: center;
    }

    .choice-button:hover {
        background-color: #ff8c00;
        color: white;
        box-shadow: 0 4px 12px rgba(255, 140, 0, 0.3);
    }

    .code-output {
        background-color: #1a1a1a;
        color: #00ff00;
        padding: 15px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        border-left: 4px solid #ff8c00;
        margin: 10px 0;
    }

    .post-card {
        background: white;
        border-radius: 8px;
        border-left: 4px solid #ff8c00;
        padding: 0;
        margin-bottom: 20px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(255, 140, 0, 0.1);
    }

    .post-header {
        padding: 12px 16px;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .post-author-info {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .post-avatar {
        font-size: 32px;
    }

    .post-author {
        font-weight: 600;
        font-size: 14px;
        color: #1a1a1a;
    }

    .post-author-sub {
        color: #65676b;
        font-size: 12px;
    }

    .post-description {
        font-size: 14px;
        margin-bottom: 8px;
        word-break: break-word;
        font-weight: 500;
        color: #1a1a1a;
    }

    .post-type-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .badge-vibe {
        background-color: #ffe8b3;
        color: #664600;
    }

    .badge-python {
        background-color: #e8f4ff;
        color: #003d7a;
    }

    .profile-header {
        background: white;
        padding: 30px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #ff8c00;
        border: 2px solid #ff8c00;
    }

    .profile-name {
        font-size: 28px;
        font-weight: 600;
        color: #1a1a1a;
    }

    .profile-stat-number {
        font-size: 24px;
        font-weight: 600;
        color: #ff8c00;
    }

    .profile-stat-label {
        font-size: 12px;
        color: #65676b;
        margin-top: 5px;
    }

    .tab-divider {
        border-bottom: 2px solid #ff8c00;
        margin: 20px 0;
    }

    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
    }

    .login-logo {
        font-size: 64px;
        font-weight: 700;
        text-align: center;
        color: #ff8c00;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"users": {}, "posts": []}
    return {"users": {}, "posts": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def init_user(nickname):
    data = load_data()
    if nickname not in data["users"]:
        data["users"][nickname] = {
            "followers": [],
            "following": [],
            "nickname": nickname,
            "created_at": datetime.now().isoformat()
        }
        save_data(data)
    return data

def get_user_posts(nickname):
    data = load_data()
    return [p for p in data["posts"] if p["author"] == nickname]

def share_code(nickname, code, code_type, description=""):
    data = load_data()
    post = {
        "id": f"{nickname}_{len(data['posts'])}_{datetime.now().timestamp()}",
        "author": nickname,
        "code": code,
        "type": code_type,
        "description": description,
        "likes": [],
        "created_at": datetime.now().isoformat()
    }
    data["posts"].append(post)
    save_data(data)
    return post

def toggle_like(post_id, nickname):
    data = load_data()
    for post in data["posts"]:
        if post["id"] == post_id:
            if nickname in post["likes"]:
                post["likes"].remove(nickname)
            else:
                post["likes"].append(nickname)
            save_data(data)
            return len(post["likes"])
    return 0

def follow_user(follower, following):
    data = load_data()
    if following not in data["users"]:
        return False
    if following not in data["users"][follower]["following"]:
        data["users"][follower]["following"].append(following)
        data["users"][following]["followers"].append(follower)
    save_data(data)
    return True

def unfollow_user(follower, following):
    data = load_data()
    if following in data["users"][follower]["following"]:
        data["users"][follower]["following"].remove(following)
        data["users"][following]["followers"].remove(follower)
    save_data(data)
    return True

def execute_code(code):
    try:
        # 임시 파일에 코드 저장
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name

        try:
            # Python 3.11로 코드 실행
            result = subprocess.run(
                ['py', '-3.11', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout
            if result.stderr:
                output += result.stderr

            return output if output.strip() else "✅ 코드가 실행되었습니다"
        finally:
            # 임시 파일 삭제
            if os.path.exists(temp_file):
                os.remove(temp_file)
    except subprocess.TimeoutExpired:
        return "❌ 에러: 코드 실행 시간 초과 (10초)"
    except Exception as e:
        return f"❌ 에러: {str(e)}"

def delete_post(post_id, nickname):
    data = load_data()
    data["posts"] = [p for p in data["posts"] if not (p["id"] == post_id and p["author"] == nickname)]
    save_data(data)
    return True

def extract_modules(code):
    """코드에서 필요한 모듈 추출"""
    import re
    lines = code.split('\n')
    modules = set()

    for line in lines:
        line = line.strip()

        # import numpy 형식
        if line.startswith('import '):
            parts = line.replace('import ', '').split(',')
            for part in parts:
                module = part.split(' as ')[0].strip()
                if module and not module.startswith('#'):
                    modules.add(module.split('.')[0])

        # from numpy import ... 형식
        elif line.startswith('from '):
            match = re.match(r'from\s+([\w.]+)\s+import', line)
            if match:
                module = match.group(1).split('.')[0]
                if module:
                    modules.add(module)

    # 표준 라이브러리 제외
    stdlib = {'sys', 'os', 'json', 're', 'math', 'random', 'datetime', 'time', 'collections', 'itertools', 'functools', 'operator', 'string', 'io', 'pickle', 'csv', 'configparser', 'logging', 'threading', 'subprocess', 'tempfile'}
    return sorted(modules - stdlib)

def get_rating(likes):
    """좋아요 수로 평점 계산 (1~5점)"""
    if likes >= 10:
        return 5.0
    elif likes >= 7:
        return 4.5
    elif likes >= 5:
        return 4.0
    elif likes >= 3:
        return 3.5
    elif likes >= 1:
        return 3.0
    else:
        return 2.0

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "coding_mode" not in st.session_state:
    st.session_state.coding_mode = None

if st.session_state.current_user is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>" * 8, unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center;'>
            <div class='login-logo'>🐍 PyShare</div>
            <div style='font-size: 18px; color: #ff8c00; font-weight: 500; margin-bottom: 30px;'>코드를 공유하고 배우는 플랫폼</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>" * 2, unsafe_allow_html=True)

        nickname = st.text_input("", placeholder="닉네임을 입력하세요", key="nickname_input")

        if st.button("▶ 시작하기", use_container_width=True):
            if nickname.strip():
                init_user(nickname)
                st.session_state.current_user = nickname
                st.session_state.coding_mode = None
                st.rerun()
            else:
                st.error("닉네임을 입력해주세요")
else:
    current_user = st.session_state.current_user

    st.markdown(f"""
    <div class='navbar'>
        <div class='navbar-logo'>🐍 PyShare</div>
        <div class='navbar-user'>👤 {current_user}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.coding_mode is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<br>" * 8, unsafe_allow_html=True)
            st.markdown("## 💻 코딩 방식을 선택하세요", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("🎨 템플릿 코딩\n(샘플 선택)", use_container_width=True, key="vibe_choice"):
                    st.session_state.coding_mode = "vibe"
                    st.rerun()

            with col_b:
                if st.button("🐍 파이썬 코딩\n(직접 입력)", use_container_width=True, key="python_choice"):
                    st.session_state.coding_mode = "python"
                    st.rerun()

            st.markdown("<br>" * 5, unsafe_allow_html=True)

            col_exit = st.columns([3, 1])[1]
            with col_exit:
                if st.button("🚪 나가기", use_container_width=True):
                    st.session_state.current_user = None
                    st.session_state.coding_mode = None
                    st.rerun()
    else:
        col_nav1, col_nav2, col_nav3 = st.columns([10, 1, 1])
        with col_nav2:
            if st.button("← 뒤로"):
                st.session_state.coding_mode = None
                st.rerun()
        with col_nav3:
            if st.button("🚪"):
                st.session_state.current_user = None
                st.session_state.coding_mode = None
                st.rerun()

        tab1, tab2, tab3, tab4 = st.tabs(["🏠 피드", "📸 프로필", "🔍 탐색", "💻 터미널"])

        with tab1:
            st.markdown("## ✨ 새 포스트 작성", unsafe_allow_html=True)
            st.markdown("<div class='tab-divider'></div>", unsafe_allow_html=True)

            if st.session_state.coding_mode == "vibe":
                st.markdown("**🎨 템플릿 선택 또는 직접 입력**")

                template_choice = st.selectbox("샘플 템플릿 선택 (선택사항)", [
                    "직접 입력",
                    "합계 계산",
                    "리스트 정렬",
                    "문자열 처리",
                    "반복문 예제"
                ])

                templates = {
                    "합계 계산": "# 1부터 100까지의 합 계산\ntotal = sum(range(1, 101))\nprint(f'합계: {total}')",
                    "리스트 정렬": "# 리스트 정렬\nnumbers = [5, 2, 8, 1, 9]\nsorted_numbers = sorted(numbers)\nprint(f'정렬된 리스트: {sorted_numbers}')",
                    "문자열 처리": "# 문자열 처리\ntext = 'Hello World'\nprint(f'길이: {len(text)}')\nprint(f'대문자: {text.upper()}')",
                    "반복문 예제": "# 반복문으로 구구단\nfor i in range(1, 10):\n    print(f'2 × {i} = {2*i}')"
                }

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("**코드 작성**")
                    if template_choice != "직접 입력":
                        default_code = templates[template_choice]
                    else:
                        default_code = ""

                    code_editor = st.text_area("", value=default_code, height=120, key="vibe_editor", label_visibility="collapsed")
                    st.session_state.vibe_code = code_editor

                with col2:
                    st.markdown("**코드 미리보기**")
                    if st.session_state.vibe_code:
                        st.code(st.session_state.vibe_code, language="python")
                    else:
                        st.info("위에 코드를 입력하세요")

                description = st.text_input("이 코드에 대한 설명을 입력하세요")

                col_ex, col_dl, col_sh = st.columns([1, 1, 1])
                with col_ex:
                    if "vibe_code" in st.session_state and st.session_state.vibe_code.strip():
                        if st.button("▶️ 실행", use_container_width=True, key="run_vibe"):
                            output = execute_code(st.session_state.vibe_code)
                            st.markdown(f"<div class='code-output'>{output}</div>", unsafe_allow_html=True)

                with col_dl:
                    if "vibe_code" in st.session_state and st.session_state.vibe_code.strip():
                        st.download_button(
                            label="⬇️ 다운로드",
                            data=st.session_state.vibe_code,
                            file_name="code.py",
                            mime="text/plain",
                            use_container_width=True,
                            key="download_vibe"
                        )

                with col_sh:
                    if st.button("📤 공유하기", use_container_width=True, key="share_vibe"):
                        if "vibe_code" in st.session_state and st.session_state.vibe_code.strip():
                            share_code(current_user, st.session_state.vibe_code, "vibe", description)
                            st.success("✅ 코드가 공유되었습니다!")
                            del st.session_state.vibe_code
                            st.rerun()
                        else:
                            st.error("코드를 입력해주세요")

            else:
                st.markdown("**🐍 직접 파이썬 코드를 작성하세요**")
                python_code = st.text_area("파이썬 코드", height=150, key="python_code", placeholder="# 여기에 파이썬 코드를 작성하세요", label_visibility="collapsed")
                description = st.text_input("이 코드에 대한 설명을 입력하세요")

                col_ex, col_dl, col_sh = st.columns([1, 1, 1])
                with col_ex:
                    if st.button("▶️ 실행", use_container_width=True, key="run_python"):
                        if python_code.strip():
                            output = execute_code(python_code)
                            st.markdown(f"<div class='code-output'>{output}</div>", unsafe_allow_html=True)
                        else:
                            st.error("코드를 입력해주세요")

                with col_dl:
                    if python_code.strip():
                        st.download_button(
                            label="⬇️ 다운로드",
                            data=python_code,
                            file_name="code.py",
                            mime="text/plain",
                            use_container_width=True,
                            key="download_python"
                        )

                with col_sh:
                    if st.button("📤 공유하기", use_container_width=True, key="share_python"):
                        if python_code.strip():
                            share_code(current_user, python_code, "python", description)
                            st.success("✅ 코드가 공유되었습니다!")
                            st.rerun()
                        else:
                            st.error("코드를 입력해주세요")

            st.markdown("<div class='tab-divider'></div>", unsafe_allow_html=True)
            st.markdown("## 🌟 팔로우 중인 사용자의 포스트", unsafe_allow_html=True)

            data = load_data()
            following_list = data["users"][current_user]["following"]

            if following_list:
                feed_posts = [p for p in data["posts"] if p["author"] in following_list]
                feed_posts = sorted(feed_posts, key=lambda x: x["created_at"], reverse=True)

                if feed_posts:
                    for post in feed_posts:
                        with st.container(border=True):
                            col1, col2 = st.columns([4, 1])

                            with col1:
                                st.markdown(f"""
                                <div>
                                    <strong>👤 {post['author']}</strong>
                                    <span style='color: #65676b; font-size: 12px;'> • {post['created_at'][:10]}</span>
                                </div>
                                """, unsafe_allow_html=True)

                                if post["description"]:
                                    st.markdown(f"**{post['description']}**")

                                badge = "🎨 템플릿" if post["type"] == "vibe" else "🐍 파이썬"
                                st.markdown(f"_{badge}_")

                                st.code(post["code"][:300] + "..." if len(post["code"]) > 300 else post["code"], language="python")

                                if st.button("⬇️ 다운로드", key=f"dl_{post['id']}", use_container_width=True):
                                    st.download_button(
                                        label="📥 코드 저장",
                                        data=post["code"],
                                        file_name=f"{post['author']}_code.py",
                                        mime="text/plain",
                                        use_container_width=True,
                                        key=f"save_{post['id']}"
                                    )

                            with col2:
                                liked = current_user in post["likes"]
                                st.markdown(f"<div style='text-align: center; font-size: 28px;'>{'❤️' if liked else '🤍'}</div>", unsafe_allow_html=True)
                                st.markdown(f"<div style='text-align: center; font-size: 14px; font-weight: 600; color: #ff8c00;'>{len(post['likes'])}</div>", unsafe_allow_html=True)

                                if st.button("좋아요", key=f"like_{post['id']}", use_container_width=True):
                                    toggle_like(post["id"], current_user)
                                    st.rerun()
                else:
                    st.info("팔로우 중인 사용자의 포스트가 없습니다")
            else:
                st.info("아직 팔로우한 사용자가 없습니다. 탐색 탭에서 사용자를 팔로우해보세요!")

        with tab2:
            data = load_data()
            user_info = data["users"][current_user]

            st.markdown(f"""
            <div class='profile-header'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;'>
                    <div style='font-size: 100px;'>👤</div>
                    <div style='flex: 1; margin-left: 20px;'>
                        <div class='profile-name'>{current_user}</div>
                        <div style='display: flex; gap: 40px; margin-top: 20px;'>
                            <div>
                                <div class='profile-stat-number'>{len(get_user_posts(current_user))}</div>
                                <div class='profile-stat-label'>게시물</div>
                            </div>
                            <div>
                                <div class='profile-stat-number'>{len(user_info['followers'])}</div>
                                <div class='profile-stat-label'>팔로워</div>
                            </div>
                            <div>
                                <div class='profile-stat-number'>{len(user_info['following'])}</div>
                                <div class='profile-stat-label'>팔로잉</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("## 📋 내 작품", unsafe_allow_html=True)
            st.markdown("<div class='tab-divider'></div>", unsafe_allow_html=True)

            user_posts = get_user_posts(current_user)

            if user_posts:
                for post in reversed(user_posts):
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])

                        with col1:
                            badge_class = "badge-vibe" if post["type"] == "vibe" else "badge-python"
                            badge_text = "🎨 템플릿" if post["type"] == "vibe" else "🐍 파이썬"
                            st.markdown(f"<span class='post-type-badge {badge_class}'>{badge_text}</span>", unsafe_allow_html=True)

                            if post["description"]:
                                st.write(f"**{post['description']}**")

                            st.code(post["code"][:250] + "..." if len(post["code"]) > 250 else post["code"], language="python")

                            col_run, col_dl, col_del = st.columns([1, 1, 1])
                            with col_run:
                                if st.button("▶️ 실행", key=f"run_{post['id']}", use_container_width=True):
                                    output = execute_code(post["code"])
                                    st.markdown(f"<div class='code-output'>{output}</div>", unsafe_allow_html=True)

                            with col_dl:
                                st.download_button(
                                    label="⬇️ 다운로드",
                                    data=post["code"],
                                    file_name="code.py",
                                    mime="text/plain",
                                    use_container_width=True,
                                    key=f"profile_dl_{post['id']}"
                                )

                            with col_del:
                                if st.button("🗑️ 삭제", key=f"del_{post['id']}", use_container_width=True):
                                    delete_post(post["id"], current_user)
                                    st.success("✅ 삭제되었습니다")
                                    st.rerun()

                            st.caption(f"📅 {post['created_at'][:10]} | ❤️ {len(post['likes'])}")

                        with col2:
                            st.metric("좋아요", len(post['likes']))
            else:
                st.info("아직 작품이 없습니다. 피드 탭에서 첫 작품을 공유해보세요!")

        with tab3:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                search_type = st.selectbox("필터", ["전체", "템플릿", "파이썬"])
            with col2:
                sort_by = st.selectbox("정렬", ["최신순", "좋아요순", "평점순"])
            with col3:
                search_term = st.text_input("사용자 검색")

            data = load_data()
            posts = data["posts"]

            if search_type == "템플릿":
                posts = [p for p in posts if p["type"] == "vibe"]
            elif search_type == "파이썬":
                posts = [p for p in posts if p["type"] == "python"]

            if search_term:
                posts = [p for p in posts if search_term.lower() in p["author"].lower()]

            if sort_by == "좋아요순":
                posts = sorted(posts, key=lambda x: len(x["likes"]), reverse=True)
            elif sort_by == "평점순":
                posts = sorted(posts, key=lambda x: get_rating(len(x["likes"])), reverse=True)
            else:
                posts = sorted(posts, key=lambda x: x["created_at"], reverse=True)

            st.markdown("<div class='tab-divider'></div>", unsafe_allow_html=True)

            if posts:
                for post in posts:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([4, 1, 1])

                        with col1:
                            st.markdown(f"""
                            <div>
                                <strong>👤 {post['author']}</strong>
                                <span style='color: #65676b; font-size: 12px;'> • {post['created_at'][:10]}</span>
                            </div>
                            """, unsafe_allow_html=True)

                            if post["description"]:
                                st.markdown(f"**{post['description']}**")

                            # 평점 표시
                            rating = get_rating(len(post["likes"]))
                            stars = "⭐" * int(rating) + ("✨" if rating % 1 else "")
                            st.markdown(f"**평가:** {stars} {rating}/5.0")

                            badge_class = "badge-vibe" if post["type"] == "vibe" else "badge-python"
                            badge_text = "🎨 템플릿" if post["type"] == "vibe" else "🐍 파이썬"
                            st.markdown(f"<span class='post-type-badge {badge_class}'>{badge_text}</span>", unsafe_allow_html=True)

                            st.code(post["code"][:200] + "..." if len(post["code"]) > 200 else post["code"], language="python")

                            # 필요한 모듈 표시
                            modules = extract_modules(post["code"])
                            if modules:
                                st.markdown(f"**📦 필요한 모듈:** {', '.join(modules)}")

                            # 복사 버튼
                            if st.button("📋 코드 복사", use_container_width=True, key=f"copy_{post['id']}"):
                                st.toast(f"✅ 복사됨: {post['author']}'s code")

                        with col2:
                            liked = current_user in post["likes"]
                            if st.button(f"{'❤️' if liked else '🤍'}", key=f"like_{post['id']}", use_container_width=True):
                                toggle_like(post["id"], current_user)
                                st.rerun()
                            st.caption(str(len(post['likes'])))

                        with col3:
                            is_following = post["author"] in data["users"][current_user]["following"]
                            follow_btn = "✔️" if is_following else "➕"

                            if post["author"] != current_user:
                                if st.button(follow_btn, key=f"follow_{post['id']}", use_container_width=True):
                                    if is_following:
                                        unfollow_user(current_user, post["author"])
                                    else:
                                        follow_user(current_user, post["author"])
                                    st.rerun()
            else:
                st.info("표시할 코드가 없습니다")

        with tab4:
            st.markdown("## 💻 모듈 설치 명령어", unsafe_allow_html=True)
            st.markdown("<div class='tab-divider'></div>", unsafe_allow_html=True)

            st.markdown("**코드를 입력하세요**")
            st.markdown("_필요한 모듈의 import문을 분석해서 설치 명령어를 생성합니다_")

            code_input = st.text_area("", placeholder="import numpy\nimport pandas as pd\nfrom sklearn import datasets", height=150, key="code_input", label_visibility="collapsed")

            if st.button("📥 설치 명령어 생성", use_container_width=True, key="gen_install"):
                if code_input.strip():
                    # import문 파싱
                    import re

                    lines = code_input.split('\n')
                    modules = set()

                    for line in lines:
                        line = line.strip()

                        # import numpy 형식
                        if line.startswith('import '):
                            parts = line.replace('import ', '').split(',')
                            for part in parts:
                                module = part.split(' as ')[0].strip()
                                if module and not module.startswith('#'):
                                    modules.add(module.split('.')[0])

                        # from numpy import ... 형식
                        elif line.startswith('from '):
                            match = re.match(r'from\s+([\w.]+)\s+import', line)
                            if match:
                                module = match.group(1).split('.')[0]
                                if module:
                                    modules.add(module)

                    # 표준 라이브러리 제외
                    stdlib = {'sys', 'os', 'json', 're', 'math', 'random', 'datetime', 'time', 'collections', 'itertools', 'functools', 'operator', 'string', 'io', 'pickle', 'csv', 'configparser', 'logging', 'threading', 'subprocess', 'tempfile'}
                    modules = modules - stdlib

                    if modules:
                        st.markdown("**📤 설치 명령어:**")

                        # 각 모듈별로 표시
                        for module in sorted(modules):
                            st.code(f"pip install {module}", language="bash")

                        st.markdown("<div class='tab-divider'></div>", unsafe_allow_html=True)

                        # 한 번에 설치
                        st.markdown("**한 번에 설치하기:**")
                        all_modules = " ".join(sorted(modules))
                        st.code(f"pip install {all_modules}", language="bash")
                    else:
                        st.info("표준 라이브러리만 사용됩니다. 추가 설치가 필요하지 않습니다.")
                else:
                    st.error("코드를 입력해주세요")
