from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.app import AppCustomer, Module, User

from werkzeug.security import generate_password_hash
from wtforms import PasswordField
from flask_admin import form
from sessions import get_session_for_app
from database import create_customer_db

# Blueprint setup with a unique name
admin_blueprint = Blueprint('app_admin', __name__, url_prefix='/app_admin')

def create_admin():
    Session = get_session_for_app()
    # Initialize the admin interface
    admin = Admin(name="Custom Admin", template_mode='bootstrap3', url='/app_admin')

    
    # Add a model view for the AppCustomer model
    admin.add_view(AppCustomerModelView(AppCustomer, Session))
    admin.add_view(ModuleModelView(Module, Session))
    admin.add_view(UserModelView(User, Session))
    return admin


class AppCustomerModelView(ModelView):
    form_columns = ('name', 'email', 'app_customer_modules')  # Explicitly include the relationship column
    
    column_list = ['name', 'email', 'app_customer_modules']

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.app_customer_modules.query_factory = lambda: Module.query.all()  # Define how to load modules in the form
        return form_class
    
    def on_model_change(self, form, model, is_created):
        session = self.session 
        if is_created:
            session.add(model)
            session.commit()  # Ensures model.id is generated

            db_type = "sqlite"  # Adjust based on requirement
            for module in model.app_customer_modules:
                create_customer_db(model.id, module.path, db_type)
    


class ModuleModelView(ModelView):
    
    def scaffold_form(self):
        form_class = super().scaffold_form()
        # You can add any customizations to the form if needed here
        return form_class
    
    
class UserModelView(ModelView):
    # Specify the fields you want to display in the admin panel
    column_list = ['id', 'user_name', 'role', 'app_customer_id']

    # Use form_columns to specify which fields should be included in the form
    form_columns = ['user_name', 'password_hash', 'role', 'app_customer_id']

    # Override the password field with the PasswordField
    form_overrides = {
        'password': PasswordField
    }

    def on_model_change(self, form, model, is_created):
        # Hash the password before saving the user model
        if form.password_hash.data:
            model.password_hash = generate_password_hash(form.password_hash.data)
        return super().on_model_change(form, model, is_created)

    # Ensure the password is handled correctly in the form
    def create_form(self):
        form = super(UserModelView, self).create_form()
        return form

    def after_model_delete(self, model):
        # You can add logic here to handle after deletion (e.g., logging, etc.)
        return super(UserModelView, self).after_model_delete(model)