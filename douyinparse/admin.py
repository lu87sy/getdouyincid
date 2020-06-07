# -*- coding: UTF-8 -*-
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from douyinparse.auth import login_required
from douyinparse.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

# @bp.route('/')
# @login_required
# def index():
#     db = get_db()
#     reqinfos = db.execute(
#         'SELECT id, username, device, cookie, x_tt_token'
#         ' FROM request_info ORDER BY id DESC'
#     ).fetchall()
#     return render_template('admin/index.html', reqinfos=reqinfos)