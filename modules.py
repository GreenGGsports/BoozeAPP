import importlib
import os 
from sessions import get_session_for_app
from models.app import Module
import logging
from flask_admin import BaseView

def import_base(module_name):
    """
    Dynamically imports the Base class from the given module name.

    :param module_name: The module from which to import the Base class (e.g., 'models.reservation')
    :return: The Base class from the specified module
    """
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        
        # Return the Base class from the module
        if hasattr(module, 'Base'):
            return module.Base
        else:
            raise AttributeError(f"The module {module_name} does not have a Base class.")
    
    except ImportError as e:
        print(f"Error importing module {module_name}: {e}")
        raise
    
    
def import_view_module(module_name):
    try:
        # Dynamically import the module from the 'views' folder
        full_module_name = f"views.{module_name}"
        module = importlib.import_module(full_module_name)

        # List to store instances of BaseView
        baseview_instances = []

        # Iterate through all classes in the module
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            # Check if the attribute is a subclass of BaseView
            if isinstance(attribute, type) and issubclass(attribute, BaseView):
                # Instantiate and add to the list of BaseView instances
                baseview_instances.append(attribute())  # Creating an instance of the BaseView subclass

        # Log if no views were found in the module
        if not baseview_instances:
            logging.info(f"{full_module_name} does not contain any Flask Admin views (subclasses of BaseView).")

        return baseview_instances

    except ImportError as e:
        logging.error(f"Error importing module {full_module_name}: {e}")
        raise

def get_all_modules(models_path="models"):
    """
    Retrieves all folder names inside the 'models' directory and returns them as 'models.<folder_name>' (except app module).

    :param models_path: The path to the models directory (default is 'models')
    :return: A list of folder names formatted as 'models.<folder_name>'
    """
    try:
        # Get all subdirectories inside the models directory
        modules = [
            f"{models_path}.{folder}"
            for folder in os.listdir(models_path)
            if os.path.isdir(os.path.join(models_path, folder)) and not folder.startswith("__") and not folder.startswith("app")
        ]
        
        return modules
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory '{models_path}' not found.")

def add_to_db(module_name):
    Session = get_session_for_app()
    folder_name = module_name.split('.')[-1]
    
    # Assuming the `Module` model has at least two fields: `name` and `path`
    module = Module(
        name=folder_name,   # Store the folder name only
        path=module_name    # Store the full path 'models.<folder_name>'
    )
    
    # Add the module to the session and commit to the database
    Session.add(module)
    Session.commit()
    print(f"Module '{folder_name}' added to the database.")


def main():
    models_path = "models"
    
    # Get all modules in the models directory
    modules = get_all_modules(models_path)
    
    # Add each module to the database
    for module in modules:
        # Add the module name to the database
        add_to_db(module)

if __name__ == "__main__":
    main()