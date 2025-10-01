# create_tables.py

from app import app, db

# アプリケーションコンテキスト内でデータベースのテーブルをすべて作成する
with app.app_context():
    db.create_all()

print("Database tables created successfully.")
