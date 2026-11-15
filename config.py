"""
数据库与 Flask 配置（单一配置入口）
修改 MySQL 密码后，所有模块自动生效。
"""
MYSQL = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'CMPD',
    'charset': 'utf8mb4',
}

FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000
DEBUG = True