import os
import sys
import random

from flask import Flask, render_template, make_response, request, redirect

from regret.models import Article, ThumbsUp
from regret.database import db_session, init_db, engine

from sqlalchemy import and_

from datetime import datetime

from pytz import timezone

app = Flask(__name__)


def get_cookie():
    return request.cookies.get('regret', None)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def index():
    ar_page = list()
    articles = Article.query.all()
    for a in articles:
        t = ThumbsUp.query.filter(and_(ThumbsUp.session_id == get_cookie(),
                                       ThumbsUp.article_id == a.id)).first()
        z = {'id': a.id, 'author': a.author, 'msg': a.msg,
             'thumbs': len(a.thumbsup), 'btn': 1 if t is None else 0}
        ar_page.append(z)
    resp = make_response(render_template('index.html', articles=ar_page))
    if not get_cookie():
        resp.set_cookie('regret', "%0x" % random.getrandbits(128))
    return resp


@app.route('/thumbs/<id>')
def thumbs(id):
    session = get_cookie()
    if session is None:
        return redirect('/')

    t = ThumbsUp.query.filter(and_(ThumbsUp.session_id == get_cookie(),
                                   ThumbsUp.article_id == id)).first()
    if t is not None:
        return redirect('/')

    t = ThumbsUp(article_id=id, session_id=session,
                 create_at=datetime.now(timezone('Asia/Seoul')))
    db_session.add(t)
    db_session.commit()
    return redirect('/')


@app.route('/post', methods=['POST'])
def post_article():
    a = Article(author=request.form['nick'], msg=request.form['msg'],
                create_at=datetime.now(timezone('Asia/Seoul')),
                session_id=get_cookie())
    db_session.add(a)
    db_session.commit()
    return redirect('/')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    app.run(host='0.0.0.0', threaded=True)
    init_db()
