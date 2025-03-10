from flask import Flask, g, request 
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from views.admin import  create_admin
from views.base import BaseAdminView
from modules import import_base 
from sessions import get_current_customer_id, get_session_for_customer, get_session_for_app
from database import create_db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Update your DB URI if necessary
app.config['SECRET_KEY'] = 'mysecret'
admin = Admin(app, name="Dynamic Admin", template_mode="bootstrap4", url="/Admin", endpoint="admin_main")

def create_app():
    create_db("app_db", "models.app")
     
    # Initialize the database

    # Register the admin Blueprint
    app_admin = create_admin()
    app_admin.init_app(app)  # Ensure this is called **only once**

    return app

@app.before_request
def before_request():
    """
    Before each request, we create and bind the session for the current customer.
    """
    # Check if the request path starts with /app_admin
    if request.path.startswith('/app_admin'):
        # Use the dev database connection for /app_admin routes
        g.session = get_session_for_app()
    else:
        # For non-admin routes, check for customer ID
        customer_id = get_current_customer_id()
        
        if customer_id:
            # Get the session for the specific customer
            g.session = get_session_for_customer(customer_id)
            BaseAdminView.register_views(admin, customer_id)
        else:
            # Raise an exception only for routes that require a customer ID (non-admin)
            raise ValueError("Customer ID is required")

@app.teardown_request
def teardown_request(exception=None):
    """
    After each request, we remove the session.
    """
    if hasattr(g, 'session'):
        g.session.remove()

# Run the application
if __name__ == '__main__':
    app = create_app()  # Create the app instance
    app.run(debug=True)  # Run the app