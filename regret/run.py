import random

from flask import Flask, render_template, make_response, request

from regret.database import db_session, init_db


app = Flask(__name__)


def get_cookie():
    return request.cookies.get('regret', None)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def index():
    resp = make_response(render_template('index.html'))
    if not get_cookie():
        resp.set_cookie('regret', "%0x" % random.getrandbits(128))
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    init_db()
