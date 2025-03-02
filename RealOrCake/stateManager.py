from cake import Cake
from randomizeCake import RandomizeCake
# Context
class GameStateManager():
    # Constructor
    def __init__(self, currentState):
        self.currentState = currentState
        self.cake = Cake()
        self.random_cake = RandomizeCake()
        self.event = None
        self.alert = None
        self.alert_active = False
    
    # Accessor
    def get_state(self):
        return self.currentState
    
    # Mutator
    def set_state(self, state):
        self.currentState = state

    def get_cake(self):
        return self.cake
    
    def set_cake(self, cake):
        self.cake = cake
    
    def get_event(self):
        return self.event
    
    def set_event(self, event):
        self.event = event

    def get_alert(self):
        return self.alert
    
    def set_alert(self, alert):
        self.alert = alert

    def get_alert_active(self):
        return self.alert_active
    
    def set_alert_active(self, alert_active):
        self.alert_active = alert_active

    def reset(self):
        self.cake.reset()
        self.set_cake(None)

    def get_randomcake(self):
        return self.random_cake
    
    def set_randomcake(self, random_cake):
        self.random_cake = random_cake
    
    def reset_randomcake(self):
        self.random_cake.reset()
        self.set_randomcake(None)