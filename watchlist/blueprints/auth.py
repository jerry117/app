from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/authlogin')
def authlogin():
    return {'code':200}

@auth.route('/authlogout')
def authlogout():
    return {'code':200}

