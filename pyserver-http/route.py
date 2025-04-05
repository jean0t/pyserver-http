from .handler import BaseHandler

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        """
        creates a new route to be accessed in the server,
        the route is saved in a dictionary with a tuple as key,
        which consists in (method, path)
        """
        self.routes[(method, path)] = handler

    def route(self, method, path):
        """
        get the route handler
        """
        return self.routes.get((method, path), BaseHandler.unknown)