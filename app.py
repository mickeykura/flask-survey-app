import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- アプリケーションの初期設定 ---
# ベースディレクトリの絶対パスを取得
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

instance_path = os.path.join(basedir, 'instance')
# フォルダが存在しない場合は作成する
os.makedirs(instance_path, exist_ok=True)

# データベースの保存先を設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'survey.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 変更点 1: データベースモデルの定義 ---
# survey.htmlのフォーム内容に合わせて、保存する列を修正します
class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device = db.Column(db.String(50), nullable=False)
    satisfaction = db.Column(db.String(50), nullable=False)
    comments_impression = db.Column(db.Text, nullable=True)
    comments_futsal = db.Column(db.Text, nullable=True)
    comments_form = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<SurveyResponse {self.name}>'


with app.app_context():
    db.create_all()
    

# --- ルーティング (ページのURLを定義) ---
@app.route('/')
def survey():
    return render_template('survey.html')

# --- 変更点 2: /submit ルートの処理 ---
# survey.htmlから送信されるすべてのデータを受け取るように修正します
@app.route('/submit', methods=['POST'])
def submit():
    # フォームから新しいデータを取得
    name = request.form['name']
    device = request.form['device']
    satisfaction = request.form['satisfaction']
    comments_impression = request.form['comments_impression']
    comments_futsal = request.form['comments_futsal']
    comments_form = request.form['comments_form']

    # 新しいモデルに合わせてオブジェクトを作成
    new_response = SurveyResponse(
        name=name, 
        device=device,
        satisfaction=satisfaction, 
        comments_impression=comments_impression,
        comments_futsal=comments_futsal,
        comments_form=comments_form
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
    """パスワード入力フォームのページを表示します。"""
    return render_template('login.html')


@app.route('/results', methods=['POST'])
def results():
    """パスワードを検証し、正しければ結果を表示、間違っていればエラーを表示します。"""
    password = request.form.get('password')
    
    if password == '085547':
        all_responses = SurveyResponse.query.all()
        return render_template('results.html', responses=all_responses)
    else:
        error = "パスワードが間違っています。"
        return render_template('login.html', error=error)



if __name__ == '__main__':
    # データベースファイルの存在を確認し、なければ作成
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    