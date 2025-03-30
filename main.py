from flask import Flask, request, render_template, make_response, abort, redirect, url_for, jsonify, session
from config import URL_DATABASE_CONNECT
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker  
from database_setup import Base, Article
from operation import get_random_error_text
from database_redis import *


app = Flask('hex_bomb')
engine = create_engine(URL_DATABASE_CONNECT)  
Base.metadata.bind = engine  
DBSession = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)  
database_session = DBSession()  


@app.route('/')
def main():# Получаем JSON-данные из запроса
    # log the user out
    return render_template('home.html')

@app.route('/home/')
def home():
    # set_cookie(key, value="", max_age=None)
    return render_template('home.html')

@app.route('/news/')
def news():
    # SET_login_redis('dwolke', 'dwolke')
    # SET_password_redis('dwolke', 'password')
    # print(GET_login_redis('dwolke'))
    # print(GET_password_redis('dwolke'))
    # print(KEY_redis('login.*'))
    return render_template('news.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/admin-panel/')
def admin_panel():
    database_session.rollback()
    articles= database_session.query(Article).all() 
    return render_template('admin-panel.html', articles=articles)

@app.route('/admin-panel/delete/<int:id>', methods=['DELETE', 'GET'])
def delete_article(id):
    database_session.rollback()
    delete = database_session.query(Article).filter_by(id=id).delete()
    database_session.commit()
    return redirect('/admin-panel/') #render_template('admin-panel.html', articles=articles)

@app.route('/admin-panel/edit/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    database_session.rollback()
    article = database_session.query(Article).filter_by(id=id)
    if request.method == 'GET':
        return render_template('edit-article.html', articles=article)
    elif request.method == 'POST':
        article.update({'title': request.form.get('name'), 'author': request.form.get('author'), 'text': request.form.get('text')})
        database_session.commit()
    return redirect('/admin-panel/')
     #render_template('admin-panel.html', articles=articles)

@app.route('/admin-panel/add/', methods=['GET', 'POST'])
def add_article():
    if request.method == 'GET':
        return render_template('add-article.html')
    elif request.method == 'POST':
        new_article = Article(id=request.form.get('id'), title=request.form.get('name') , author=request.form.get('author') , text=request.form.get('text'))
        database_session.add(new_article)
        database_session.commit()
    return redirect('/admin-panel/')

@app.route('/log_in/', methods=['GET', 'POST'])
def log_in():
    #request.form - мульти словарь с формой, котрую мы отправили(работать как с обычнм словарем)
    if request.method == "POST":
        SET_login_redis(request.form.get('login'), request.form.get('login'))
        SET_password_redis(request.form.get('login'), request.form.get('password'))

    return render_template('log_in.html')

@app.route('/sign_up/')
def sign_up():
    return render_template('sign_up.html')

@app.route('/change_theme/')
def change_theme():
    if request.cookies.get('ispink'):
        res = make_response("Changing of the color")
        res.set_cookie('ispink', 'true', max_age=0)
    else:
        res = make_response("Changing of the color")
        res.set_cookie('ispink', 'true', max_age=3600)
    return res

# @app.route('/bckkp/')
# def bckkp():
#     return render_template('/bckkp.html')

@app.route('/articles/')
def articles():
    database_session.rollback()
    articles = database_session.query(Article).all() 
    return render_template('articles.html', articles=articles)

@app.errorhandler(404)
def not_found_error(*args, **kwargs):
    return render_template('error.html', error_code=404, error_text=get_random_error_text()), 404

@app.errorhandler(403)
def forbidden_error(*args, **kwargs):
    return render_template('error.html', error_code=403, error_text=get_random_error_text()), 403

@app.errorhandler(405)
def bad_access(*args, **kwargs):
    return render_template('error.html', error_code=405, error_text=get_random_error_text()), 405

@app.errorhandler(500)
def server_error(*args, **kwargs):
    return render_template('error.html', error_code=500, error_text=get_random_error_text()), 500

@app.errorhandler(502)
def not_implemented_error(*args, **kwargs):
    return render_template('error.html', error_code=502, error_text=get_random_error_text()), 502


if __name__ == '__main__':
    app.run(debug=True, port=5006)
