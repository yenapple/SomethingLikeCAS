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

'''이제부터 몇 가지 핵심 논의를 하고서 그 방향성에 맞게 개발해나가야 한다. 
Solve mode, Expand mode, User -defined functions 등이 그것이다.'''