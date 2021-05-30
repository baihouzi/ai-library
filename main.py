import cv2
from flask import Flask, url_for, render_template, request, redirect, jsonify, session
import datetime
import db
import face
import os
import time
from const import *

app = Flask(__name__)  # 代码示例化
app.secret_key = os.urandom(24)  # 设置密钥为24位随机字符

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(
    seconds=1)  #设置flask缓存刷新时间

users = db.all_user()
sync_keys = [user['name'] for user in users]  #读取用户的人脸信息

face_db = face.FaceDB(FACE_ENCODING_PATH, sync_keys=sync_keys)  #读取人脸编码数据


# 定义跟路由为登陆页面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # 登陆验证
        if 'user_id' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

    else:
        admin_id = request.form['userId']
        if db.admin_all(admin_id):
            password = db.admin_all(admin_id)[0]['admin_pwd']
            if password == request.form['password']:
                # 将管理员登陆状态写入session
                session['user_id'] = 1
                # 将管理员姓名写入session
                session['username'] = db.admin_all(admin_id)[0]['admin_name']
                # 将上次登陆时间写入session
                session['last_login_time'] = db.admin_all(
                    admin_id)[0]['last_login_time']
                login_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                           time.localtime())
                db.login_time(time=login_time, userid=admin_id)
                return jsonify({'code': 200})
            else:
                return jsonify({'code': 400, 'message': '密码错误'})
        else:
            return jsonify({'code': 400, 'message': '用户名错误'})


# 路由到主页
@app.route('/index')
def index():
    if 'user_id' in session:
        book_num = db.book_num()[0]['COUNT(*)']
        user_num = db.user_num()
        borrow_num = db.borrow_num()[0]['COUNT(*)']
        return render_template('index.html',
                               book_num=book_num,
                               user_num=user_num,
                               borrow_num=borrow_num)
    else:
        return redirect(url_for('login'))


# 图书列表
@app.route('/books')
def list_book():
    if 'user_id' in session:
        book_num = int(db.book_num()[0]['COUNT(*)'])
        if book_num % 3 == 0:
            page_max = book_num // 3
        else:
            page_max = book_num // 3 + 1
        page = int(request.args.get('page', 1))
        books = db.list_book(page)
        return render_template('book/list.html',
                               books=books,
                               page_max=page_max,
                               page=page)
    else:
        return redirect(url_for('login'))


# 添加图书
@app.route('/books/create', methods=['GET', 'POST'])
def create_book():
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('book/create.html')
        else:
            db.add_book(title=request.form['title'],
                        author=request.form['author'],
                        serial=request.form['serial'],
                        intro=request.form['intro'])

            return jsonify({'code': 200, 'message': '添加成功'})
    else:
        return redirect(url_for('login'))


# 查询图书
@app.route('/books/query', methods=['GET', 'POST'])
def query_book():
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('book/query.html')
        else:
            if request.form.get('select') == '书名查询':
                books = db.query_book(title=request.form['key'],
                                      author='',
                                      serial='')
            elif request.form.get('select') == '作者查询':
                books = db.query_book(title='',
                                      author=request.form['key'],
                                      serial='')
            else:
                books = db.query_book(title='',
                                      author='',
                                      serial=request.form['key'])
            if books:
                return render_template('book/query.html', books=books)
            else:
                return jsonify({'code': 400, 'message': '没有找到这本书'})
    else:
        return redirect(url_for('login'))


# 更新图书信息
@app.route('/books/update', methods=['GET', 'POST'])
def update_book():
    if 'user_id' in session:
        if request.method == 'GET':
            book_id = request.args.get('id', '')
            book = db.get_book(int(book_id))

            return render_template('book/update.html', book=book)
        else:
            db.update_book(book_id=int(request.args.get('id', '')),
                           title=request.form['title'],
                           author=request.form['author'],
                           serial=request.form['serial'],
                           intro=request.form['intro'])

            return jsonify({'code': 200, 'message': '编辑成功'})
    else:
        return redirect(url_for('login'))


# 删除图书
@app.route('/books/delete', methods=['POST'])
def delete_book():
    if 'user_id' in session:
        db.delete_book(book_id=int(request.args.get('id', '')))

        return jsonify({'message': '删除成功'})
    else:
        return redirect(url_for('login'))


# 借书/还书
@app.route('/books/op', methods=['GET', 'POST'])
def op_book():
    if 'user_id' in session:
        status = request.args.get('status', '')
        if request.method == 'GET':
            book_id = request.args.get('id', '')
            book = db.get_book(book_id)
            # borrow_status = db.get_book(book_id)['borrower']
            if book['borrower'] != -1:  # returning
                user = db.get_face(book['borrower'])
                borrow_status = '1'
            else:  # borrowing
                borrow_status = '-1'
                username = request.args.get('username', '')
                if username != '':
                    user = db.get_face_by_name(username)
                else:
                    user = {}

            return render_template('book/op.html',
                                   book_id=book_id,
                                   book=db.get_book(book_id),
                                   borrower=user,
                                   borrow_status=borrow_status,
                                   status=status)
        else:
            book_id = int(request.form['book_id'])
            book = db.get_book(book_id)
            db.update_book_borrower(
                book_id=book_id,
                borrower_name=request.form['borrower'],
            )
            # borrow_status = db.get_book(book_id)['borrower']
            if book['borrower'] != -1:
                lend_time = int(book['lend_time'])
                borrow_time = book['update_time']
                now_time = datetime.datetime(time.localtime()[0],
                                             time.localtime()[1],
                                             time.localtime()[2])
                lending_time = (now_time - borrow_time).days
                db.return_status(book_id=book_id,
                                 return_name=request.form['borrower'])
                if lending_time > lend_time:
                    id = db.get_face_by_name(
                        name=request.form['borrower'])['id']
                    db.delete_face(id)
                    return jsonify({
                        'code': 400,
                        'message': '由于该用户逾期未归还，改账号已被删除，请重新添加！'
                    })
                else:
                    return jsonify({'code': 200, 'message': '成功还书！'})
            else:
                borrow_time = book['update_time']
                # sdate  = datetime.datetime.strptime(borrow_time,'%Y-%m-%d %H:%M:%S')
                return_time = borrow_time + datetime.timedelta(
                    days=int(request.form['lend_time']))

                db.borrow_status(book_id=book_id,
                                 borrower_name=request.form['borrower'],
                                 lend_time=int(request.form['lend_time']),
                                 return_time=return_time)

            face.clear_snapshot()

            return jsonify({
                'code':
                200,
                'message':
                '%s成功借书%d天！' %
                (request.form['borrower'], int(request.form['lend_time']))
            })
    else:
        return redirect(url_for('login'))


# 人脸比对
@app.route('/books/compare/<book_id>', methods=['POST'])
def compare(book_id):
    if 'user_id' in session:
        snap_path = face.snapshot(face_db)

        if snap_path is None:
            return redirect('/books/op?status=0&id={}'.format(book_id))

        img = cv2.imread(snap_path)
        match_id = face_db.compare_face(img)

        if match_id == -1:
            return redirect('/books/op?status=0&id={}'.format(book_id))

        return redirect('/books/op?status=1&id={}&username={}'.format(
            book_id, match_id))
    else:
        return redirect(url_for('login'))


#借书记录
@app.route('/record', methods=['GET', 'POST'])
def record():
    if 'user_id' in session:
        if request.method == 'GET':
            borrow_num = int(db.borrow_num()[0]['COUNT(*)'])
            if borrow_num % 10 == 0:
                page_max = borrow_num // 10
            else:
                page_max = borrow_num // 10 + 1
            page = int(request.args.get('page', 1))
            borrow_books = db.borrow_books(page)
            return render_template('book/record.html',
                                   borrow_books=borrow_books,
                                   page_max=page_max,
                                   page=page)
        else:
            if request.form.get('select') == '姓名':
                user = db.get_face_by_name(name=request.form['key'])
                if user:
                    if user['status'] == 0:
                        return jsonify({'code': 400, 'message': '该用户没有借书记录！'})
                    else:
                        borrow_books = db.borrow_books_id(int(user['id']))
                        print(borrow_books)
                        return render_template('book/record.html',
                                               borrow_books=borrow_books,
                                               page_max=1,
                                               page=1)
                else:
                    return jsonify({'code': 400, 'message': '该用户不存在'})
            elif request.form.get('select') == '学号':
                user = db.get_face_by_num(num=request.form['key'])
                if user:
                    if user['status'] == 0:
                        return jsonify({'code': 400, 'message': '该用户没有借书记录！'})
                    else:
                        borrow_books = db.borrow_books_id(user['id'])
                        return render_template('book/record.html',
                                               borrow_books=borrow_books,
                                               page_max=1,
                                               page=1)
                else:
                    return jsonify({'code': 400, 'message': '该用户不存在'})

    else:
        return redirect(url_for('login'))


# 用户列表
@app.route('/users')
def list_user():
    if 'user_id' in session:
        user_num = db.user_num()
        if user_num % 10 == 0:
            page_max = user_num // 10
        else:
            page_max = user_num // 10 + 1
        page = int(request.args.get('page', 1))

        users = db.list_face(page)
        return render_template('user/list.html',
                               users=users,
                               page_max=page_max,
                               page=page)
    else:
        return redirect(url_for('login'))


# 添加用户
@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if 'user_id' in session:
        if request.method == 'GET':
            status = request.args.get('status', '')

            if status is None:
                return render_template('user/register.html', status=0)
            elif status == 'ok':
                return render_template('user/register.html', status=1)
            elif status == 'fail':
                return render_template('user/register.html', status=2)
            else:
                return render_template('user/register.html', status=0)
        else:
            username = request.form['username']
            student_num = request.form['student_num']
            user_class = request.form['class']
            college = request.form['college']
            db.add_face(username=username,
                        student_num=student_num,
                        user_class=user_class,
                        college=college)
            face_db.register_face_from_snapshot(username)

            face.clear_snapshot()

            # users = db.list_face()
            return redirect('/users')
    else:
        return redirect(url_for('login'))


# 比对结果
@app.route('/users/snapshot', methods=['POST'])
def snapshot():
    if 'user_id' in session:
        snap_path = face.snapshot(face_db)

        return redirect('/users/create?status={}'.format(
            'ok' if snap_path is not None else 'fail'))
    else:
        return redirect(url_for('login'))


# 删除用户
@app.route('/users/delete', methods=['GET'])
def delete_user():
    if 'user_id' in session:
        db.delete_face(face_id=int(request.args.get('id', '')))

        return redirect('/users')
    else:
        return redirect(url_for('login'))


# 退出登陆
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
  
    return redirect(url_for('login'))


# 添加管理员
@app.route('/admin/add', methods=['GET', 'POST'])
def add_admin():
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('admin/add.html')
        else:
            admin_id = request.form['admin_id']
            admin_name = request.form['admin_name']
            admin_pwd = request.form['admin_pwd']
            db.add_admin(admin_id=admin_id,
                         admin_name=admin_name,
                         admin_pwd=admin_pwd)
            return redirect('/admin/list')
    else:
        return redirect(url_for('login'))


# 管理员列表
@app.route('/admin/list', methods=['GET'])
def list_admin():
    if 'user_id' in session:
        admins = db.list_admin()
        # print(admins)
        return render_template('admin/list.html', admins=admins)
    else:
        return redirect(url_for('login'))


# 删除管理员
@app.route('/admin/delete', methods=['GET'])
def delete_admin():
    if 'user_id' in session:
        db.delete_admin(admin_id=int(request.args.get('id', '')))

        return redirect('/admin/list')
    else:
        return redirect(url_for('login'))