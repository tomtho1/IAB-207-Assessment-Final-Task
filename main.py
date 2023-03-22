from flask import Flask


def create_app():
    app = Flask(__name__)
    return app


from event import create_app

if __name__ == '__main__':
    n_app = create_app()
    n_app.run(debug=True)
