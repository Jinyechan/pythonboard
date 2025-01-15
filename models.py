import mysql.connector
from datetime import datetime


class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="10.0.66.27",
                user="chris",
                password="1234",
                database="board_db2"
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as error:
            print(f"데이터베이스 연결 실패: {error}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def get_all_posts(self):
        try:
            self.connect()
            sql = "SELECT * FROM posts"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"게시글 조회 실패: {error}")
            return []
        finally:
            self.disconnect()

    def login_user(self, user_id, user_password):
        try:
            self.connect()
            sql = "SELECT * FROM customer_ips WHERE user_id = %s AND user_password = %s"
            values = (user_id, user_password)
            self.cursor.execute(sql, values)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"계정 조회 실패: {error}")
            return []
        finally:
            self.disconnect()

    def insert_post(self, title, content, filename):
        try:
            self.connect()
            sql = "INSERT INTO posts (title, content, filename, created_at) VALUES (%s, %s, %s, %s)"
            values = (title, content, filename, datetime.now())
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 추가 실패: {error}")
            return False
        finally:
            self.disconnect()

    def get_post_by_id(self, id):
        try:
            self.connect()
            sql = "SELECT * FROM posts WHERE id = %s"
            value = (id,)
            self.cursor.execute(sql, value)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"게시글 조회 실패: {error}")
            return None
        finally:
            self.disconnect()

    def insert_comment(self, post_id, username, content):
        try:
            self.connect()
            sql = "INSERT INTO comments (post_id, username, content, created_at) VALUES (%s, %s, %s, %s)"
            values = (post_id, username, content, datetime.now())
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"댓글 추가 실패: {error}")
            return False
        finally:
            self.disconnect()

    def get_comments_by_post_id(self, post_id):
        try:
            self.connect()
            sql = "SELECT * FROM comments WHERE post_id = %s ORDER BY created_at DESC"
            value = (post_id,)
            self.cursor.execute(sql, value)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"댓글 조회 실패: {error}")
            return []
        finally:
            self.disconnect()

    def insert_customer_ip(self, userid, username, password):
        try:
            self.connect()
            sql = "INSERT INTO customer_ips (user_id, user_name, user_password, requested_at) VALUES (%s, %s, %s, %s)"
            values = (userid, username, password, datetime.now())
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            print(f"계정 등록 실패: {error}")
            return False
        finally:
            self.disconnect()

    def update_post(self, post_id, title, content, filename):
        try:
            self.connect()
            sql = "UPDATE posts SET title = %s, content = %s, filename = %s, updated_at = %s WHERE id = %s"
            values = (title, content, filename, datetime.now(), post_id)
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 수정 실패: {error}")
            return False
        finally:
            self.disconnect()

    def delete_post(self, post_id):
        try:
            self.connect()
            sql = "DELETE FROM posts WHERE id = %s"
            value = (post_id,)
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 삭제 실패: {error}")
            return False
        finally:
            self.disconnect()

    def increment_post_views(self, post_id):
        try:
            self.connect()
            sql = "UPDATE posts SET views = views + 1 WHERE id = %s"
            value = (post_id,)
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"조회수 증가 실패: {error}")
            return False
        finally:
            self.disconnect()
