from flask import Blueprint, render_template, request

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/create', methods=['GET', 'POST'])
def create():
    print('Method type: ', request.method)


@bp.route('/history', methods=['GET', 'POST'])
def history():
    return render_template("history.html", title="Your History | Elevental")
