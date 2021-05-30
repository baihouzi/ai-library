import traceback

import pymysql

from const import *


# books



def borrow_books_id(id):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute(
            'SELECT * FROM books,faces WHERE books.borrower=faces.id AND faces.id=%d' % id)
        borrow_books = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()
    return borrow_books
def borrow_books(page):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')
    page_num = (page - 1) * 10
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute(
            'SELECT * FROM books,faces WHERE books.borrower=faces.id ORDER BY books.update_time DESC LIMIT %d, 10' % page_num)
        borrow_books = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return borrow_books


def borrow_num():
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:

        sql = "SELECT COUNT(*) FROM books WHERE borrower!=-1"

        cursor.execute(sql)
        borrow_num = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return borrow_num


def book_num():
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:

        sql = "SELECT COUNT(*) FROM books"

        cursor.execute(sql)
        booknum = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return booknum

    def user_num():
        db = pymysql.connect(host=MYSQL_HOST,
                             port=MYSQL_PORT,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:

        sql = "SELECT COUNT(*) FROM faces"

        cursor.execute(sql)
        usernum = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return usernum


def query_book(title='', author='', serial=''):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        if title is None:
            title = ''
        if author is None:
            author = ''
        if serial is None:
            serial = ''
        titles='%'+title+'%'
        sql = "SELECT * FROM books WHERE title LIKE '%s' OR author='%s' OR serial='%s'" % (
            titles, author, serial)

        cursor.execute(sql)
        books = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return books


def list_book(page):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')
    page_num = (page - 1) * 3
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('SELECT * FROM books ORDER BY id LIMIT %d, 3' %
                       page_num)
        books = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return books


def get_book(book_id):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)
    
    try: 
        cursor.execute("SELECT * FROM books WHERE id='%s'"  % book_id)
        book = cursor.fetchone()
        # print(book)
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()
    return book


def add_book(title, author, serial, intro=''):
    insert_tuple = (title, author, serial, intro)

    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor()

    try:
        cursor.execute('''
        INSERT INTO books(title, author, serial, intro)
        VALUES('%s', '%s', '%s', '%s')
        ''' % insert_tuple)
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def update_book(book_id, title, author, serial, intro=''):
    update_tuple = (title, author, serial, intro, book_id)

    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor()

    try:
        cursor.execute('''
        UPDATE books SET 
        title='%s', 
        author='%s',
        serial='%s',
        intro='%s'
        WHERE id=%d
        ''' % update_tuple)
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def delete_book(book_id):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('DELETE FROM books WHERE id=%s' % book_id)
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def update_book_borrower(book_id, borrower_name):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM books WHERE id='%s'" % book_id)
        book = cursor.fetchone()

        if book['borrower'] == -1:
            # borrowing
            cursor.execute("SELECT * FROM faces WHERE name='%s'" %
                           borrower_name)
            user = cursor.fetchone()

            update_tuple = (user['id'], book_id)
        else:
            # returning
            update_tuple = (-1, book_id)

        cursor.execute("UPDATE books SET borrower=%d WHERE id='%s'" %
                       update_tuple)
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


# users


def list_face(page):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')
    page_num = (page - 1) * 10
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('SELECT * FROM faces ORDER BY class, student_num LIMIT %d, 10' %
                       page_num)
        users = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return users


def get_face(user_id):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('SELECT * FROM faces WHERE id=%s' % user_id)
        user = cursor.fetchone()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return user


def get_face_by_name(name):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM faces WHERE name='%s'" % name)
        user = cursor.fetchone()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return user

def get_face_by_num(num):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM faces WHERE student_num='%s'" % num)
        user = cursor.fetchone()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return user


def add_face(username='', student_num='', user_class='', college=''):
    # insert_tuple = (
    #     username,
    # )

    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor()

    try:
        cursor.execute('''
        INSERT INTO faces(name,student_num,class,college)
        VALUES("%s","%s","%s","%s")
        ''' % (username, student_num, user_class, college))
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def delete_face(face_id):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('DELETE FROM faces WHERE id=%s' % face_id)
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def login_time(time='', userid=''):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute(
            "UPDATE admin SET last_login_time='%s' WHERE admin_id='%s'" %
            (time, userid))
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def user_num():
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:

        sql = "SELECT COUNT(*) FROM faces"

        cursor.execute(sql)
        user_num = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return user_num[0]['COUNT(*)']





def borrow_status(book_id, borrower_name, lend_time,return_time):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM books WHERE id=%d" % book_id)
        book = cursor.fetchone()
        cursor.execute("SELECT * FROM faces WHERE name='%s'" % borrower_name)
        user = cursor.fetchone()
        user_id = user['id']

        cursor.execute("UPDATE faces SET status=status+1 WHERE id=%d" %
                       user_id)
        cursor.execute("UPDATE books SET lend_time=%d,return_time='%s' WHERE id=%d" %
                       (lend_time,return_time,book_id))
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def return_status(book_id, return_name):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM books WHERE id=%d" % book_id)
        book = cursor.fetchone()
        cursor.execute("SELECT * FROM faces WHERE name='%s'" % return_name)
        user = cursor.fetchone()
        user_id = user['id']

        cursor.execute("UPDATE faces SET status=status-1 WHERE id=%d" %
                       user_id)
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def admin_all(admin_id):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:

        cursor.execute('SELECT * FROM admin WHERE admin_id=%s' % admin_id)
        admin_all = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return admin_all


def all_admin():
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:


        cursor.execute('SELECT admin_id FROM admin')
        all_admin = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return all_admin


def borrow_users():
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('SELECT * FROM faces WHERE status!=0')
        borrow_users = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return borrow_users


def all_user():
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('SELECT * FROM faces')
        users = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return users


def add_admin(admin_id='', admin_name='', admin_pwd=''):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor()

    try:
        cursor.execute('''
        INSERT INTO admin(admin_id,admin_name,admin_pwd)
        VALUES("%s","%s","%s")
        ''' % (admin_id, admin_name, admin_pwd))
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()


def list_admin():
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('SELECT * FROM admin')
        admins = cursor.fetchall()
    except Exception as err:
        traceback.print_exc()
    finally:
        db.close()

    return admins


def delete_admin(admin_id):
    db = pymysql.connect(host=MYSQL_HOST,
                         port=MYSQL_PORT,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWORD,
                         db=MYSQL_DB,
                         charset='utf8')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute('DELETE FROM admin WHERE admin_id=%s' % admin_id)
        db.commit()
    except Exception as err:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()