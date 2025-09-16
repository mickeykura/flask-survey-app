import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- アプリケーションの初期設定 ---
# ベースディレクトリの絶対パスを取得
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# データベースの保存先を設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'survey.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- データベースモデルの定義 ---
# 回答を保存するためのテーブルを定義します
class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    satisfaction = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<SurveyResponse {self.name}>'

# --- ルーティング (ページのURLを定義) ---
# ルートURL ('/') にアクセスされたときの処理
@app.route('/')
def survey():
    return render_template('survey.html')

# '/submit' にフォームデータがPOSTされたときの処理
@app.route('/submit', methods=['POST'])
def submit():
    # フォームからデータを取得
    name = request.form['name']
    satisfaction = request.form['satisfaction']
    comments = request.form['comments']

    # 新しい回答オブジェクトを作成
    new_response = SurveyResponse(name=name, satisfaction=satisfaction, comments=comments)

    # データベースに保存
    db.session.add(new_response)
    db.session.commit()

    # 送信完了ページにリダイレクト
    return redirect(url_for('success'))

# '/success' にアクセスされたときの処理
@app.route('/success')
def success():
    return render_template('success.html')

# '/results' にアクセスされたときの処理
@app.route('/results')
def results():
    # データベースからすべての回答を取得
    all_responses = SurveyResponse.query.all()
    return render_template('results.html', responses=all_responses)


if __name__ == '__main__':
    # データベースファイルの存在を確認し、なければ作成
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    