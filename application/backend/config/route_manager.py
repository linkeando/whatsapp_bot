import pkgutil
import importlib
from flask import Blueprint


class RouteManager:
    def __init__(self, app, package_name):
        self.app = app
        self.package_name = package_name
        self.routes_without_prefix = ['home']

    def register_routes(self):
        package = importlib.import_module(self.package_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{self.package_name}.{module_name}")
            if hasattr(module, "init_app"):
                blueprint = Blueprint(module_name, __name__)
                module.init_app(blueprint)
                url_prefix = f"/{module_name}" if module_name not in self.routes_without_prefix else ""
                self.app.register_blueprint(blueprint, url_prefix=url_prefix)