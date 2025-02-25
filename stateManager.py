# Context
class GameStateManager():
    # Constructor
    def __init__(self, currentState):
        self.currentState = currentState
    
    # Accessor
    def get_state(self):
        return self.currentState
    
    # Mutator
    def set_state(self, state):
        self.currentState = state