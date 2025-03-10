from flask_admin import Admin, BaseView, expose
from flask import session, redirect, url_for
from sessions import get_session_for_app
from models.app import AppCustomer
from sqlalchemy.orm import joinedload
from modules import import_view_module
import logging

class BaseAdminView(BaseView):
    """Base class for all module views in Flask-Admin."""
    
    def is_accessible(self):
        """Override this method to define accessibility logic."""
        customer_id = session.get("customer_id")
        allowed_modules = session.get("allowed_modules", [])
        return self.module_name in allowed_modules if customer_id else False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to home if access is denied."""
        return redirect(url_for("index"))

    @classmethod
    def register_views(cls, admin, customer_id):
        """
        Dynamically registers views for a customer based on available modules.
        
        :param admin: Flask-Admin instance
        :param customer_id: Current customer ID to register views for
        """
        # Set customer ID in the session
        session["customer_id"] = customer_id
        
        # Get session for the app
        Session = get_session_for_app()
        
        # Query the customer's modules
        customer = Session.query(AppCustomer).options(joinedload(AppCustomer.app_customer_modules)) \
            .filter_by(id=customer_id).first()
        
        if not customer:
            logging.error(f"Customer with ID {customer_id} not found.")
            return

        modules = customer.app_customer_modules

        
        # Clear previously registered views
        admin._views.clear()
        
        # Dynamically import and register views based on the modules
        for module in modules:
            module_name = module.name  # Assuming `name` is the name of the module view
            logging.info(f"Attempting to import view for module {module_name}")
            
            # Dynamically import the view module
            try:
                module_views = import_view_module(f"{module_name}")  # Adjust if views are in a subfolder
                if module_views:
                    for module_view in module_views:
                        # Register the view to Flask-Admin
                        admin.add_view(module_view)  # Pass customer_id if needed for view initialization
                        logging.info(f"Successfully registered view for module {module_name}")
                else:
                    logging.warning(f"No view found for module {module_name}")
            except Exception as e:
                logging.error(f"Error importing or registering view for module {module_name}: {e}")

