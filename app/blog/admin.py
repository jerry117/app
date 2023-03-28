from flask_login import login_required
from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')