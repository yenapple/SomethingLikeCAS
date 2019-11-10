import Context
Context_space = []
# Existing Contexts

CurrentContext = None # Now using Context

def Run():
    # User Interface to execute on certain context
    pass

def Close_context():
    global CurrentContext
    CurrentContext = None


class Context: # class of Contexts

    def __init__(self):

        global Context_space
        self.namespace = []
        Context_space.append(self)

    def load(self):

        global CurrentContext
        CurrentContext = self

