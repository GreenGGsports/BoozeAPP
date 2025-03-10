from flask_admin import BaseView, expose

class SomeModuleView(BaseView):
    @expose('/')
    def index(self, customer_id):
        # You can access customer_id here if needed for dynamic rendering
        return self.render('index.html', message=f"Hello from SomeModuleView for Customer {customer_id}!")
