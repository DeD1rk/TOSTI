
class Widget:

    def __init__(self):
        self.widgets = dict()

    def add_widget(self, func, takes_context=False, name=None, width=1):
        if name is None:
            name = func.__name__

        func.takes_context = takes_context
        func.width = width

        self.widgets[name] = func

    def get_widgets(self):
        return self.widgets


widget = Widget()
