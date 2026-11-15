"""
数据库连接工具层
提供 query / query_one / execute / executemany 四个基础函数。
所有 SQL 都通过参数化执行，防止注入。
"""
import pymysql
from config import MYSQL


def get_conn():
    return pymysql.connect(
        host=MYSQL['host'], port=MYSQL['port'],
        user=MYSQL['user'], password=MYSQL['password'],
        database=MYSQL['database'], charset=MYSQL['charset'],
        cursorclass=pymysql.cursors.DictCursor,
    )


def query(sql, args=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchall()
    finally:
        conn.close()


def query_one(sql, args=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchone()
    finally:
        conn.close()


def execute(sql, args=None):
    """执行单条写 SQL，返回受影响行数。"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def execute_returning_id(sql, args=None):
    """执行写 SQL 并返回自增主键 lastrowid。"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def executemany(sql, args_list):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.executemany(sql, args_list)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()