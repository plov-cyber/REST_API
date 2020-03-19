from flask import Flask, make_response, jsonify
import jobs_api
import users_api
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
