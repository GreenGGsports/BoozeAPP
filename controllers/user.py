from flask import flash,Blueprint, request, jsonify, current_app, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Identity, RoleNeed, UserNeed, identity_changed, identity_loaded
from models.app import User
from database import db 


user_ctrl = Blueprint('user_ctrl', __name__, url_prefix='/user')

class user(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.user_name = user.user_name
        self.role = user.role
        
# Function to initialize LoginManager
def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            user = db.session.query(User).get(user_id)
            if user:
                current_app.logger.info('authentication succesfull')
                return user(user)
            return None
        finally:
            db.session.close()
