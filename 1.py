import sqlite3
import os



def check_db():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_file = os.path.join(basedir, 'dev_database.db')
    if not os.path.exists(db_file):
        # 常见原因 1：Flask 把数据库建到了 instance 文件夹下，你没找对地方
        print(f"❌ 找不到数据库文件: {db_file}")
        return

    print(f"📂 发现数据库文件: {db_file}")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 查询数据库中所有的表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("Empty! 😶 数据库里没有任何表。")
    else:
        print("✅ 数据库中的表有:")
        for table in tables:
            print(f" - {table[0]}")
            # 如果存在 users 表，顺便看看表结构
            if table[0] == 'users' or table[0] == 'user':
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                print(f"   📊 结构: {[col[1] for col in columns]}")

    conn.close()

if __name__ == "__main__":
    check_db()