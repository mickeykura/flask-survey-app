import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- アプリケーションの初期設定 ---
app = Flask(__name__)

# Renderの環境変数からデータベースURLを取得。なければローカルのSQLiteを使う
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Renderで提供されるPostgreSQLのURL形式をSQLAlchemyが認識できるように修正
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    

    
"""
else:
    # ローカル開発用の設定（DATABASE_URLがない場合）
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'survey.db')
"""

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- データベースモデルの定義 ---
class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device = db.Column(db.String(50), nullable=False)
    satisfaction = db.Column(db.String(50), nullable=False)
    comments_impression = db.Column(db.Text, nullable=True)
    comments_futsal = db.Column(db.Text, nullable=True)
    comments_form = db.Column(db.Text, nullable=True)
    coop = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<SurveyResponse {self.name}>'

# --- ルーティング (ページのURLを定義) ---
@app.route('/')
def survey():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    # フォームから新しいデータを取得
    name = request.form['name']
    device = request.form['device']
    satisfaction = request.form['satisfaction']
    comments_impression = request.form['comments_impression']
    comments_futsal = request.form['comments_futsal']
    comments_form = request.form['comments_form']
    coop = request.form['coop']
    
    # 新しいモデルに合わせてオブジェクトを作成
    new_response = SurveyResponse(
        name=name, 
        device=device,
        satisfaction=satisfaction, 
        comments_impression=comments_impression,
        comments_futsal=comments_futsal,
        comments_form=comments_form,
        coop=coop
    )

    # データベースに保存
    db.session.add(new_response)
    db.session.commit()

    # 送信完了ページにリダイレクト
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/results', methods=['POST'])
def results():
    password = request.form.get('password')
    
    if password == '085547':
        # データベースから全ての回答を取得
        all_responses = SurveyResponse.query.all()
        return render_template('results.html', responses=all_responses)
    else:
        error = "パスワードが間違っています。"
        return render_template('login.html', error=error)

# アプリケーションの実行
if __name__ == '__main__':
    # アプリケーションコンテキスト内でデータベースを作成
    with app.app_context():
        db.create_all()
    app.run(debug=True)