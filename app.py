from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
from models import DBManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # 세션을 위한 비밀 키 설정
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

manager = DBManager()


# 로그인 기능
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userid')
        user_password = request.form.get('password')
        user = manager.login_user(user_id, user_password)
        if user:
            session['user_id'] = user.get('user_id')
            session['user_name'] = user['user_name']
            return redirect(url_for('index'))
    return render_template('login.html')


# 로그아웃 기능
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 회원가입 기능
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error="비밀번호가 일치하지 않습니다.")

        if manager.insert_customer_ip(userid, username, password):
            return redirect(url_for('login'))
        return render_template('signup.html', error="회원가입 실패.")
    return render_template('signup.html')


# 메인 페이지
@app.route('/')
def index():
    posts = manager.get_all_posts()
    return render_template('index.html', posts=posts)


# 게시글 추가
@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files.get('file')
        filename = file.filename if file else None

        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if manager.insert_post(title, content, filename):
            return redirect("/")
        return "게시글 추가 실패", 400
    return render_template('add.html')


# 게시글 수정
@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = manager.get_post_by_id(id)

    if not post:
        return "게시글을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files.get('file')
        filename = None
        if file and file.filename:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if manager.update_post(id, title, content, filename):
            return redirect(url_for('index'))
        return "게시글 수정 실패", 400
    return render_template('edit.html', post=post)


# 게시글 삭제
@app.route('/post/delete/<int:id>')
def delete_post(id):
    if manager.delete_post(id):
        return redirect(url_for('index'))
    return "게시글 삭제 실패", 400


# 게시글 상세보기 및 댓글 추가
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    post = manager.get_post_by_id(id)
    comments = manager.get_comments_by_post_id(id)

    if not post:
        return "게시글을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        username = request.form.get('username')
        comment_content = request.form.get('comment_content')

        if not comment_content or not username:
            return render_template('view.html', post=post, comments=comments, error="모든 필드를 입력하세요.")

        if manager.insert_comment(post_id=id, username=username, content=comment_content):
            return redirect(url_for('view_post', id=id))

    return render_template('view.html', post=post, comments=comments)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)