class Controller(object):

    def __init__(self, model, view):
        if model is None:
            raise TypeError("Error, model is None")
        if view is None:
            raise TypeError("Error, view is None")
        self.model = model
        self.view = view
